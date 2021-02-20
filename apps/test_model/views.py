import json
import hashlib
import datetime

from django.views import View
from urllib.parse import quote
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from rest_framework.serializers import ModelSerializer, DictField

from .models import TestModel
from viewsets import MyGenericViewSet
from apps.core.mixins import LogRequestMixin
from apps.utils.views import LoginRequiredJsonMixin, LoginRequiredMixin


class IndexView(View):
    def get(self, request):
        a = [
            {"type": "一条", "sales": 38},
            {"type": "二条", "sales": 52},
            {"type": "三条", "sales": 61},
            {"type": "四条", "sales": 145},
            {"type": "五条", "sales": 48},
            {"type": "六条", "sales": 38},
            {"type": "七条", "sales": 38},
            {"type": "八条", "sales": 38}
        ]
        return JsonResponse(a, safe=False)

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


