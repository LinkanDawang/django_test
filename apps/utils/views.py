from functools import wraps

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


class LoginRequiredPageMixin:
    """
    未登录调用接口跳转到登入页
    """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required(view)


def login_required_json(view_func):
    """
    用户未登入返回提示的json信息，可当做装饰器装饰在View下某一个具体的请求function [get, post, put...]
    :param view_func:
    :return:
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({"code": 1, "msg": "用户未登录"})
    return wrapper


class LoginRequiredJsonMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required_json(view)
