import re

from django.http import JsonResponse
from django.views import View
from django import db

from apps.utils.responses import CustomResponse
from .models import Users


class RegisterView(View):
    def post(self, request):
        # get account info
        params = request.JSON
        username = params.get('username')
        phonenum = params.get('phonenum')
        email = params.get('email', None)
        password = params.get('password')

        try:
            phonenum = re.match(r'^1[35789]\d{9}$', phonenum).group(0)
        except Exception as e:
            return CustomResponse(code=400, msg='手机号码格式错误')

        try:
            user = Users.objects.create_user(
                username=username,
                cell_phone=phonenum,
                email=email,
                password=password
            )
        except db.IntegrityError:
            return CustomResponse(code=400, msg='用户已经被注册')

        token = user.generate_activate_token()

        # return JsonResponse({'code': 200, 'msg': 'ok', 'data': {'name': 'Leslie'}})
        return CustomResponse(data=params, code=200)

