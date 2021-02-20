from functools import wraps

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


class LoginRequiredMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required(view)


def login_required_json(view_func):
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
