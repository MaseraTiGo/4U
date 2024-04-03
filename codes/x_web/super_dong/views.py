from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'index.html')


def adminer(request):
    return render(request, 'adminer.html')
