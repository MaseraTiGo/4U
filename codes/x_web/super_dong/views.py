from django.shortcuts import render

from super_dong.gui.admin.money.simple_line_chart import \
    gen_html as gen_line_html
from super_dong.gui.admin.money.yield_per_10_kilo import \
    gen_html as gen_histogram_html


# Create your views here.


def index(request):
    return render(request, 'index.html')


def adminer(request):
    return render(request, 'adminer.html')


def shit_trend_line(request):
    days = request.GET.get('d')
    days = days if days else 30
    gen_line_html(int(days))

    return render(request, 'bokeh_ui/lines/my_line.html')


def shit_per_10_kilo(request):
    gen_histogram_html()

    return render(request, 'bokeh_ui/lines/my_histogram.html')
