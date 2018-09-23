from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from .models import Current, Overview, Information

# Create your views here.
def index(request):
    return render(request, 'spidermonitor/index.html')

def get(request, maxid):
    spider = get_current_spider()
    if spider == None:
        spider = {'name': '当前爬虫未设置'}
        infos = {}
    else:
        infos = Information.objects.filter(id__gt=maxid, own=spider).order_by('-time') # 按时间降序排列
    # return 'im the spidermonitor/get/'
    return render_to_response('spidermonitor/json', {'spider': spider, 'infos': infos})

def detail(request, infoid):
    info = Information.objects.get(id=infoid)
    return render(request, 'spidermonitor/detail.html', {'info': info})

def get_current_spider():
    try:
        c = Current.objects.get(id=1)
        return c.current
    except:
        return None
