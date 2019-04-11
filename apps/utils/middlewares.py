import json

from django.utils.deprecation import MiddlewareMixin


class OldCustomMiddleware(MiddlewareMixin):
    """
    自定义中间价(旧版写法)
    统一把ContentType为application/json的数据转换成json,放到request.JSON里
    """
    def process_request(self, request, *args, **kwargs):
        if request.content_type == 'application/json':
            try:
                request.JSON = json.loads(request.body)
            except:
                request.JSON = {}

    def process_response(self, request, response):
        if request.content_type == 'application/json':
            try:
                request.JSON = json.loads(request.body)
            except:
                request.JSON = {}
        return response

    def process_exception(self, request, exception):
        pass


class NewCustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        # 请求之前的处理代码写在这里
        if request.content_type == 'application/json':
            try:
                request.JSON = json.loads(request.body)
            except Exception as e:
                request.JSON = {}

        # 处理请求
        response = self.get_response(request)

        # 请求之后的代码写在这里
        pass

        return response

