import json
import hashlib
import datetime
import oss2
from django.shortcuts import render

from django.views import View
from urllib.parse import quote
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from rest_framework.serializers import ModelSerializer, DictField
from django.conf import settings

from .models import TestModel
from viewsets import MyGenericViewSet
from apps.core.mixins import LogRequestMixin
from apps.utils.views import LoginRequiredJsonMixin, LoginRequiredPageMixin, login_required_json


class Index2View(View):
    @login_required_json
    def get(self, request):
        return render(request, "upload2.html")


class IndexView(View):
    def get(self, request):
        from aliyunsdkcore import client
        from aliyunsdksts.request.v20150401 import AssumeRoleRequest
        role_arn = 'acs:ram::1416120736225768:role/oss-uploader'
        oss_access_key = settings.AWS_ACCESS_KEY_ID
        oss_secret_key = settings.AWS_SECRET_ACCESS_KEY
        clt = client.AcsClient(
            settings.ALI_OSS_RAM_ACCESS_KEY, settings.ALI_OSS_RAM_SECRET_KEY,
            "cn-shanghai",
            session_period=300
        )
        req = AssumeRoleRequest.AssumeRoleRequest()

        # 设置返回值格式为JSON。
        req.set_accept_format('json')
        req.set_RoleArn(role_arn)
        req.set_RoleSessionName('django-test')
        # req.set_Policy(policy_text)
        body = clt.do_action_with_exception(req)

        # 使用RAM账号的AccessKeyId和AccessKeySecret向STS申请临时token。
        resp_data = json.loads(oss2.to_unicode(body))
        result = {
            "code": 0,
            "RequestId": resp_data["RequestId"],
            "SecurityToken": resp_data["Credentials"]["SecurityToken"],
            "AccessKeyId": resp_data["Credentials"]["AccessKeyId"],
            "AccessKeySecret": resp_data["Credentials"]["AccessKeySecret"],
            "bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "region": "cn-shanghai"
        }
        return JsonResponse(result)

    def post(self, request):
        # from django.core.files.storage import default_storage
        # with open("/Users/leslie/Desktop/drony.apk", "rb") as f:
        #     url = default_storage.save(f.name, f)
        return JsonResponse({"code": 0, "message": "", "data": request.POST})


def test():
    """billnumber=SMG1908280000003&barCode=6923450656181&nodeCode=1016&sign=6ac3ee4c93e8c21a078449b9b25dfdb5 """
    sign = "fea543a774737365e66f9898e3fec437"
    uid = "1011438291"
    skey = "HX3DD114D007c1"
    source = "billnumber=SMG1908260000004&barCode=6923450656181&nodeCode=1045"
    dd = {"uid": "1011438291", "billnumber": "SMG1908260000004", "barCode": "6923450656181", "nodeCode": "1045"}

    ss = [
        "uid=1011438291&billnumber=SMG1908260000004&barCode=6923450656181&nodeCode=1045",
        "uid=1011438291&billnumber=SMG1908260000004&nodeCode=1045&barCode=6923450656181",
        "uid=1011438291&barCode=6923450656181&billnumber=SMG1908260000004&nodeCode=1045",
        "uid=1011438291&barCode=6923450656181&nodeCode=1045&billnumber=SMG1908260000004",
        "uid=1011438291&nodeCode=1045&barCode=6923450656181&billnumber=SMG1908260000004",
        "uid=1011438291&nodeCode=1045&billnumber=SMG1908260000004&barCode=6923450656181"
    ]

    for x in ["1011438291", "SMG1908260000004", "6923450656181", "1045"]:
        demo = ["1011438291", "SMG1908260000004", "6923450656181", "1045"].remove(x)
        for y in demo:
            pass

    for i in ss:
        ostring = quote(i).lower()
        # ostring = quote(json.dumps(dd)).lower()
        md5_func = hashlib.md5()
        md5_func.update(ostring.encode())
        true_sign = md5_func.hexdigest().lower()

        # print(sign)
        print(true_sign)


class TestDRFSerialiaer(ModelSerializer):

    class Meta:
        model = TestModel
        fields = "__all__"


class TestCctionSerialiaer(TestDRFSerialiaer):
    conf_json = DictField(read_only=True)

    def to_representation(self, instance):
        
        ret = super(TestCctionSerialiaer, self).to_representation(instance)
        conf = instance.conf
        ret["conf_json"] = json.loads(conf)
        return ret

    class Meta:
        model = TestModel
        fields = ("conf", "conf_json")


class TestDRFViewSet(MyGenericViewSet, ListModelMixin):
    queryset = TestModel.objects.all()
    serializer_class = {
        "default": TestDRFSerialiaer,
        "test_action": TestCctionSerialiaer
    }

    @action(detail=False, methods=["GET"])
    def test_action(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(data=serializer.data)


class WatchGtViewSet(LogRequestMixin, MyGenericViewSet, ListModelMixin):
    queryset = TestModel.objects.all()
    serializer_class = {
        "default": TestDRFSerialiaer
    }
    logging_actions = ["list", ]

    def list(self, request, *args, **kwargs):
        return render(request, "Watch.html")


