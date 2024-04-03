from django.shortcuts import render

from super_dong.gui.admin.money.simple_line_chart import gen_html


# Create your views here.


def index(request):
    return render(request, 'index.html')


def adminer(request):
    return render(request, 'adminer.html')


def shit_trend_line(request):
    days = request.GET.get('d')
    days = days if days else 30
    gen_html(int(days))

    return render(request, 'bokeh_ui/lines/my_line.html')
