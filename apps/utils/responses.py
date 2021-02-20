import json

from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder


class CustomResponse(HttpResponse):
    def __init__(self, data=None, code=200, msg=None, json_dumps_params=None, **kwargs):
        form_data = {"code": code, "msg": 'success'}
        if code != 200:
            form_data.update({'code': code})
            if msg:
                form_data.update({'msg': msg})
            else:
                form_data.update({'msg': 'fail'})

        if data:
            form_data['data'] = data

        if json_dumps_params is None:
            json_dumps_params = {}

        kwargs.setdefault('content_type', 'application/json')

        res_data = json.dumps(form_data, cls=DjangoJSONEncoder, **json_dumps_params)

        super().__init__(content=res_data, **kwargs)


