# encoding:utf-8
from django.http import HttpResponse

#测试主页接口
def index(request):
    if request.method=='GET':
        return HttpResponse("请求成功！请求方法为GET")
    if request.method=='POST':
        return HttpResponse("请求成功！请求方法为POST")
    else:
        return HttpResponse("请求方法错误")