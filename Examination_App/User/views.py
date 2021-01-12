from django.shortcuts import render
from django.http import HttpResponse
from User.models import T_user_info
from User.models import T_purchase_history
from User.models import T_purchase_state
from Examination.models import T_test_paper
import datetime
import json
from django.http import JsonResponse
from django.core import serializers
import time
# Create your views here.
#用户注册接口
def register(request):
    if request.method=='POST':
        registration_date = request.POST.get('registration_date')
        user_real_name=request.POST.get('user_real_name')
        wechat_id=request.POST.get('wechat_id')
        phone_number=request.POST.get('phone_number')
        identity_card=request.POST.get('identity_card')
        number = T_user_info.objects.filter(user_id__startswith=registration_date).count()
        result = 1+number
        numbers = str(result).zfill(4)
        date = registration_date.replace("-","")
        user_id = date+numbers
        print(user_id)
        if  T_user_info.objects.filter(phone_number=phone_number) or T_user_info.objects.filter(wechat_id=wechat_id):
            return HttpResponse("该号码已被注册")
        else:
            user=T_user_info(user_id=user_id,wechat_id=wechat_id,user_real_name=user_real_name,phone_number=phone_number,identity_card=identity_card,registration_date=registration_date)
            print(user.identity_card)
            user.save()
            return HttpResponse("注册成功")
    else:
        return HttpResponse("请求方法错误！")

#用户登录接口
def login(request):
    if request.method=='POST':
        identity_card = request.POST.get('identity_card')
        phone_number = request.POST.get('phone_number')
        isuser = T_user_info.objects.filter(identity_card=identity_card).first()
        if isuser!=None:
            if phone_number == isuser.phone_number:
                if isuser.login_state != "1":
                    user = T_user_info.objects.filter(phone_number=phone_number).first()
                    user.login_state=1
                    user.save()
                    print("用户登陆状态写入成功！")
                    return HttpResponse("登陆成功")
                else:
                    return HttpResponse("该用户已登录")
        else:
            return HttpResponse("当前用户不存在")
    else:
        return HttpResponse("请求方式错误")


#用户注销接口
def log_out(request):
    if request.method=='GET':
        identity_card = request.GET.get('identity_card')
        print(identity_card)
        phone_number = request.GET.get('phone_number')
        print(phone_number)
        isuser = T_user_info.objects.filter(identity_card=identity_card).first()
        if isuser != None:
            if phone_number == isuser.phone_number:
                user = T_user_info.objects.filter(phone_number=phone_number).first()
                user.login_state = 0
                user.save()
                print("用户登陆状态写入成功！")
                return HttpResponse("注销成功")
        else:
            return HttpResponse("当前用户不存在")
    else:
        return HttpResponse("请求方式错误")

#登陆后的用户请求题库
def get_test_paper(request):
    if request.method=='POST':
        user_id = request.POST.get('user_id')
        question_category_id = request.POST.get('question_category_id')
        primkey=user_id+question_category_id
        print(primkey)
        if T_purchase_state.objects.filter(purchase_state_id=primkey):
            test_paper = T_test_paper.objects.filter(question_category_id=question_category_id)
            data={
                "ispurchase":True,
                "test_list":[]
            }
            for i in range(len(test_paper)):
                id = test_paper[i].test_paper_id
                name = test_paper[i].test_paper_id_name
                dit = {
                    "test_paper_id":id,
                    "test_paper_name":name
                }
                data["test_list"].append(dit)
            print(json.dumps(data))
            return JsonResponse(data,safe=False)
        else:
            data = {
                "ispuchase": False,
            }
            return JsonResponse(data, safe=False)
    else:
        return HttpResponse("请求方式错误")

#用户购买接口
def purchase(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        question_category_id = request.POST.get('question_category_id')
        purchase_date = request.POST.get('purchase_date')
        purchase_day = request.POST.get('purchase_day')#返回购买天数
        t_purchase_history = T_purchase_history(user_id=user_id,question_category_id=question_category_id,purchase_date=purchase_date)
        t_purchase_history.save()
        ans_time_stamp=datetime.datetime.strptime(purchase_date, "%Y-%m-%d")
        delta = datetime.timedelta(days=int(purchase_day))
        t_purchase_state = T_purchase_state()
        primkey = user_id+question_category_id
        print(primkey)
        if T_purchase_state.objects.filter(purchase_state_id=primkey):
            t_purchase_state.purchase_state_id = user_id + question_category_id
            t_purchase_state.user_id = user_id
            t_purchase_state.question_category_id = question_category_id
            t_purchase_state.expiry_date = ans_time_stamp + delta
            t_purchase_state.save()
            print("购买状态已更新")
        else:
            t_purchase_state.purchase_state_id=user_id+question_category_id
            t_purchase_state.user_id = user_id
            t_purchase_state.question_category_id=question_category_id
            t_purchase_state.expiry_date=ans_time_stamp+delta
            print("购买状态已写入")
            t_purchase_state.save()

        return HttpResponse("购买记录写入成功")
    else:
        return  HttpResponse("请求方式错误")