# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/12/2019 10:56 AM'

from django.http import HttpResponse
from django.shortcuts import render
from ..models import Beauty
import os


def api_doc(request):
    return HttpResponse('welcome to the api_doc page')


def upload_pic(request):
    if request.method == 'POST':
        new_img = Beauty(
            img=request.FILES.get('img'),
            name=request.FILES.get('img').name
        )
        new_img.save()
    return render(request, 'uploadimg.html', {})


def show_pic(request):
    img_s = Beauty.objects.all()
    content = {
        'img_s': img_s,
    }
    for i in img_s:
        print('================>', i.img)
    return render(request, 'showimg.html', content)
