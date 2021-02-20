import json
from io import BytesIO, StringIO
from django import forms
from urllib.parse import parse_qs
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.deprecation import MiddlewareMixin


class UploadFileForm(forms.Form):
    file = forms.FileField()


class UploadFileMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if request.method.upper() == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                f_content = request.FILES["file"].read()
                f_name = request.FILES["file"].name
                url = default_storage.save(f_name, f)
                request.POST["file_url"] = url

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


class OldCustomMiddleware(MiddlewareMixin):
    """
    自定义中间价(旧版写法)
    统一把ContentType为application/json的数据转换成json,放到request.JSON里
    """
    def process_request(self, request, *args, **kwargs):
        if request.content_type == 'application/json':
            try:
                request.JSON = quit(request.body)
            except:
                request.JSON = {}
            print(request.JSON)

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
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        try:
            request.JSON = json.loads(request.body)
        except Exception as e:
            request.JSON = {}

        # handle the request
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        # print(response.getvalue())

        return response

