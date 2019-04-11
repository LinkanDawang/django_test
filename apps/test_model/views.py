from django.views import View
from django.http import JsonResponse
from django.shortcuts import render

from .models import StudentsInfoModel


class IndexView(View):
    def get(self, request):
        action = request.GET.get('action')

        if action == 'add':
            res = StudentsInfoModel.objects.create(
                name='LeslieChan',
                grade=6,
                c_lass=1,
                gender=1
            )
            print(res)
        else:
            res = ''
        print('----------------------------')
        return render(request, 'index.html')

