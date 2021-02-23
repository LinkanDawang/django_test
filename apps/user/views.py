import re
import itsdangerous

from django import db
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from apps.user.models import User
from apps.utils.responses import CustomResponse


class RegisterView(View):
    def post(self, request):
        # get account info
        username = request.POST.get('username')
        # phonenum = request.POST.get('phonenum')
        email = request.POST.get('email', None)
        password = request.POST.get('password')

        if not all([username, email, password]):
            return JsonResponse(data={"code": 404, "msg": "参数不全"})

        # try:
        #     phonenum = re.match(r'^1[35789]\d{9}$', phonenum).group(0)
        # except Exception as e:
        #     return CustomResponse(code=400, msg='手机号码格式错误')
        try:
            print(email)
            email = re.match(
                r'^[A-Za-z0-9]+([_\.][A-Za-z0-9]+)*@([A-Za-z0-9\-]+\.)+[A-Za-z]{2,6}$',
                email).group(0)
        except Exception as e:
            return JsonResponse(data={"code": 404, "msg": "邮箱格式错误"})

        try:
            user = User.objects.create_user(
                username=username,
                # cell_phone=phonenum,
                email=email,
                password=password
            )
        except db.IntegrityError:
            return JsonResponse(data={"code": 404, "msg": "用户已经存在"})
        user.is_active = False
        user.save()

        token = user.generate_activate_token()

        html_body = '<h1>尊敬的用户 %s, 感谢您的注册！</h1>' \
                    '<br/><p>请点击此链接激活您的帐号<a href="http://leslie.eacho.online/api/users/active/%s">' \
                    'http://leslie.eacho.online/api/users/active/%s</a></p>' % (username, token, token)

        send_mail('账号激活', '', settings.EMAIL_FROM, [email], html_message=html_body)

        return JsonResponse(data={"code": 200, "msg": "ok"})


class ActiveView(View):
    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            result = serializer.loads(token)
        except itsdangerous.SignatureExpired:
            return HttpResponse("激活超时")
        try:
            user = User.objects.get(id=result["confirm"])
        except User.DoesNotExist:
            return HttpResponse('用户不存在')
        if user.is_active:
            return HttpResponse('用户已激活')
        user.is_active = True
        user.save()
        return HttpResponse("激活成功")


class LoginView(View):
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not all([username, password]):
            return JsonResponse({"code": 404, "msg": "参数不全"})

        user = authenticate(request, username=username, password=password)
        if not user:
            return JsonResponse({"code": 404, "msg": "用户名或密码错误"})
        if not user.is_active:
            return JsonResponse({"code": 404, "msg": "用户未激活"})
        login(request, user)

        return JsonResponse({"code": 200, "msg": "ok"})


class LoginJsonView(View):
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not all([username, password]):
            return JsonResponse(data={"code": 404, "msg": "参数不全"})

        user = authenticate(request, username=username, password=password)
        if not user:
            return JsonResponse(data={"code": 404, "msg": "用户名或密码错误"})
        if not user.is_active:
            return JsonResponse(data={"code": 404, "msg": "用户未激活"})
        login(request, user)

        return JsonResponse(data={"code": 200, "msg": "Success"})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return JsonResponse()

