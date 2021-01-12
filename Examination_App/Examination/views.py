from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from Examination.models import T_question_info, T_test_paper,T_question_category,T_category_one,T_category_two,T_category_three
from User.models import T_purchase_state
from django.core import serializers
import json


# Create your views here.
# 向数据库中添加题目的接口
def add_examination(request):
    if request.method == 'POST':
        exam = T_question_info()
        exam.type = request.POST.get("type")
        exam.desc = request.POST.get("desc")
        exam.right_answer = request.POST.get("right_answer")
        exam.answerA = request.POST.get("answerA")
        exam.answerB = request.POST.get("answerB")
        exam.save()
        print(exam.desc)
        return HttpResponse(exam.type, exam.desc)
    else:
        return HttpResponse("用户请求方式错误")



# 取数据库中的题目的接口
def get_examination(request):
    if request.method == 'GET':
        data = {}
        panduan = T_question_info.objects.filter(type="判断题").all()
        xuanze = T_question_info.objects.filter(type='单选题').all()
        duoxuan = T_question_info.objects.filter(type='多选题').all()
        data['panduan'] = json.loads(serializers.serialize('json', panduan))
        data['danxuan'] = json.loads(serializers.serialize('json', xuanze))
        data['duoxuan'] = json.loads(serializers.serialize('json', duoxuan))
        return JsonResponse(data)
    else:
        return HttpResponse("请求方式错误！")


def get_test_paper_id(request):
    if request.method == 'GET':
        category = T_question_category.objects.filter().all()
        result=[]
        ste_1=set()
        for i in range(len(category)):
            id_1 = category[i].question_category_id[0:2]
            if id_1 not in ste_1:
                id_2 = category[i].question_category_id[2:]
                name_1 = category[i].question_category_name[:-2]
                dit = {"id": id_1,
                       "name": name_1,
                       "list": [
                           {
                               "id": "01",
                               "name": "新培",
                               "list": []
                           },
                           {
                               "id": "02",
                               "name": "复审",
                               "list": []
                           },
                       ]
                       }
                test_paper_list = T_test_paper.objects.filter(test_paper_id__startswith=
                                                            id_1).all()
                # print(test_paper_list[0].test_paper_id)
                for i in range(len(test_paper_list)):
                    test_paper_id = test_paper_list[i].test_paper_id
                    test_paper_name = test_paper_list[i].test_paper_id_name
                    temp={
                        "id":test_paper_id,
                        "name":test_paper_name,
                        "list": [
                            {
                                "id": "01",
                                "name": "新培",
                                "list": []
                            },
                            {
                                "id": "02",
                                "name": "复审",
                                "list": []
                            },
                        ]
                    }
                    # print(test_paper_id)
                    # print(test_paper_name)
                    teps = test_paper_id[2:4]
                    if teps=="01":
                        dit["list"][0]["list"].append(temp)
                    else:
                        dit["list"][1]["list"].append(temp)
                # print(dit)
                if len(test_paper_list)!=0:
                    result.append(dit)
                else:
                    pass
                # print(result)
                ste_1.add(id_1)
            else:
                pass
        results = json.dumps(result)
        return JsonResponse(results,safe=False)
    else:
        return HttpResponse("请求方式错误")


def get_all_testpaper(request):
    if request.method=='GET':
        id_1 = T_category_one.objects.filter().all()
        id_2 = T_category_two.objects.filter().all()
        id_3 = T_category_three.objects.filter().all()
        print(id_1[0].category_one_id)
        result=[]
        for i in range(len(id_1)):
            data = {
                "id": id_1[i].category_one_id,
                "name": id_1[i].category_one_name,
                "list_1":[]
            }
            for j in range(len(id_2)):
                temp_1 = {
                    "id":id_2[j].category_two_id,
                    "name":id_2[j].category_two_name,
                    "list_2":[]
                }
                data["list_1"].append(temp_1)
                for k in range(len(id_3)):
                    temp_2={
                        "id":id_3[k].category_three_id,
                        "name":id_3[k].category_three_name,
                        "list_3":[]
                    }
                    data["list_1"][j]["list_2"].append(temp_2)
                    id = id_1[i].category_one_id+id_2[j].category_two_id+id_3[k].category_three_id
                    test_paper_list = T_test_paper.objects.filter(test_paper_id__startswith=id).all()
                    for m in range(len(test_paper_list)):
                        temp_3={
                            "id":test_paper_list[m].test_paper_id,
                            "name":test_paper_list[m].test_paper_name
                        }
                        data["list_1"][j]["list_2"][k]["list_3"].append(temp_3)
                    print(id)


        print(data)
        return JsonResponse(data,safe=False)
    else:
        return HttpResponse("请求方式错误")

def get_user_test_no(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        # 已购买列表
        d = T_purchase_state.objects.filter(user_id=user_id).all()
        # 类别列表
        c1 = T_category_one.objects.filter().all()
        c2 = T_category_two.objects.filter().all()
        c3 = T_category_three.objects.filter().all()
        # 总列表
        aq = T_question_category.objects.filter().all()
        # 所有试题
        atq = T_test_paper.objects.filter().all()
        # 类别字典
        c1_dic = c2_dic = c3_dic = {}
        # 已购买类别
        has_test_paper_list = []
        # 总类别
        all_has_test_paper_list = []
        # 未购买类别
        no_has_test_paper_list = []
        # 所有试题
        all_test_paper = {}
        # 第一类ID对应名字
        for index in range(len(c1)):
            c1_dic[str(c1[index].category_one_id)] = str(
                c1[index].category_one_name)
        # 第二类ID对应名字
        for index in range(len(c2)):
            c2_dic[str(c2[index].category_two_id)] = str(
                c2[index].category_two_name)
        # 第三类ID对应名字
        for index in range(len(c3)):
            c3_dic[str(c3[index].category_three_id)] = str(
                c3[index].category_three_name)
        # 所有试题对应的名字和编号
        for index in range(len(atq)):
            if atq[index].question_category_id not in all_test_paper.keys():
                all_test_paper[atq[index].question_category_id] = [
                    {
                        "id": atq[index].test_paper_id,
                        "name":atq[index].test_paper_name
                    }
                ]
            else:
                all_test_paper[atq[index].question_category_id].append({
                    "id": atq[index].test_paper_id,
                    "name": atq[index].test_paper_name
                })

        # 获取所有的类别表
        for index in range(len(aq)):
            temp = {}
            all_has_test_paper_list.append(
                str(aq[index].question_category_id))
            temp[aq[index].question_category_id
                 ] = aq[index].question_category_name
        # 获取已购买类别
        for index in range(len(d)):
            has_test_paper_list.append(str(d[index].question_category_id))
        # 列表去重
        has_test_paper_list = set(has_test_paper_list)
        all_has_test_paper_list = set(all_has_test_paper_list)
        # 计算未购买列表
        temp_no_has_test_paper_list = list(
            all_has_test_paper_list.difference(has_test_paper_list))
        # 开始整合未购买类别
        # 如果都购买了,则返回值为空(需要更新一下开发文档)
        if len(temp_no_has_test_paper_list) == 0:
            tempdata = {"has_data": False, "data_list": []}
            return JsonResponse(tempdata, safe=False)

        # 首先按照升序对未购买列表进行排序,升序排序
        temp_no_has_test_paper_list.sort()
        # 循环未购买列表进行判断,采用多轮循环，方便理解
        # 第一轮循环先添加一大类
        temp_one = []
        temp_two = []
        for item in temp_no_has_test_paper_list:
            if item[:2] not in temp_one:
                temp = {
                    "id": item[:2],
                    "name": c1_dic[item[:2]],
                    "list": [
                        {
                            "id": item[2:4],
                            "name":c2_dic[item[2:4]],
                            "list":[
                                {
                                    "id": item[4:],
                                    "name":c3_dic[item[4:]],
                                    "list":all_test_paper[item]
                                }
                            ]
                        }
                    ]
                }
                no_has_test_paper_list.append(temp)
            else:
                if item[:4] not in temp_two:
                    temp_two.append(item[:4])
                    for index in range(len(no_has_test_paper_list)):
                        if no_has_test_paper_list[index]['id'] == item[:2]:
                            temp = {
                                "id": item[2:4],
                                "name": c2_dic[item[2:4]],
                                "list": [
                                    {
                                        "id": item[4:],
                                        "name":c3_dic[item[4:]],
                                        "list":all_test_paper[item]
                                    }
                                ]
                            }
                            no_has_test_paper_list[index]['list'].append(temp)
                else:
                    for index_one in range(len(no_has_test_paper_list)):
                        if no_has_test_paper_list[index_one]['id'] == item[:2]:
                            for index_two in range(len(no_has_test_paper_list[index_one]['list'])):
                                if no_has_test_paper_list[index_one]['list'][index_two]['id'] == item[2:4]:
                                    temp = {
                                        "id": item[4:],
                                        "name": c3_dic[item[4:]],
                                        "list": all_test_paper[item]
                                    }
                                    no_has_test_paper_list[index_one]['list'][index_two]['list'].append(
                                        temp)

        # no_has_test_paper_list 已经处理完毕,整理完，即可序列化返回s
        tempdata = {"has_data": True, "data_list": no_has_test_paper_list}
        return JsonResponse(tempdata, safe=False)

# def get_user_test_no(request):
#     if request.method=='GET':
#         user_id = request.GET.get('user_id')
#         d = T_purchase_state.objects.filter(user_id=user_id).all()
#         li = []
#         for i in range(len(d)):
#             li.append(d[i].question_category_id)
#         print(li)
#
#         id_1 = T_category_one.objects.filter().all()
#         id_2 = T_category_two.objects.filter().all()
#         id_3 = T_category_three.objects.filter().all()
#         # print(id_1[0].category_one_id)
#         # for s in range(len(li)):
#         #     print(li[s])
#         for i in range(len(id_1)):
#            data = {
#                "id": id_1[i].category_one_id,
#                "name": id_1[i].category_one_name,
#                "list_1": []
#            }
#            for j in range(len(id_2)):
#                temp_1 = {
#                    "id": id_2[j].category_two_id,
#                    "name": id_2[j].category_two_name,
#                    "list_2": []
#                }
#                data["list_1"].append(temp_1)
#                for k in range(len(id_3)):
#                    if id_1[i].category_one_id+id_2[j].category_two_id+id_3[k].category_three_id in li:
#                        temp_s={
#                            "data":None
#                        }
#                        data["list_1"][j]["list_2"].append(temp_s)
#                    else:
#                        temp_2 = {
#                            "id": id_3[k].category_three_id,
#                            "name": id_3[k].category_three_name,
#                            "list_3": []
#                        }
#                        data["list_1"][j]["list_2"].append(temp_2)
#                        id = id_1[i].category_one_id+id_2[j].category_two_id+id_3[k].category_three_id
#                        test_paper_list = T_test_paper.objects.filter(test_paper_id__startswith=id).all()
#                        for m in range(len(test_paper_list)):
#                            temp_3 = {
#                                "id": test_paper_list[m].test_paper_id,
#                                "name": test_paper_list[m].test_paper_id_name
#                            }
#                            data["list_1"][j]["list_2"][k]["list_3"].append(temp_3)
#                        # print(id)
#
#
#
#
#         # print(data)
#         # for i in li:
#         #     id_2=i[:2]
#         #     id_3=i[-2:]
#         #     for j in range(len(data["list_1"])):
#         #         if data["list_1"][j]["id"]==id_2 and data["list_1"][j]["list_2"][0]["id"]==id_3:
#         #             del data["list_1"][j]["list_2"][0]
#         #
#         #         elif data["list_1"][j]["id"]==id_2 and data["list_1"][j]["list_2"][1]["id"]==id_3:
#         #             del data["list_1"][j]["list_2"][1]
#         #
#         #         else:
#         #             pass
#         #     if len(data["list_1"][i]["list_2"][j]["list_3"]) == 0:
#         #         # del data["list_1"][i]
#         #         print(data["list_1"])
#         #     else:
#         #         pass
#         print(data)
#
#
#
#
#         return JsonResponse(data,safe=False)
#     else:
#         return HttpResponse("请求方式错误")
#根据用户ID取该用户购买的题库并分类
def get_user_test(request):
    if request.method=='GET':
        user_id = request.GET.get('user_id')
        print(user_id)
        if T_purchase_state.objects.filter(user_id=user_id):
            category_objects = T_purchase_state.objects.filter(user_id=user_id)
            result=[]
            for i in range(len(category_objects)):
                result.append(category_objects[i].question_category_id)
            print(result)
            # data = []
            # for i in range(len(category_id)):
            #     id = category_id[i].question_category_id
            #     ca = T_question_category.objects.filter(question_category_id=id).first()
            #     name = ca.question_category_name
            #     dit={
            #         "id":id[:2],
            #         "name":name[:-2],
            #         "list":[]
            #     }
            #     if
            #     print(dit)
            category = T_question_category.objects.filter(question_category_id__in=result).all()
            print(category)
            result = []
            ste_1 = set()
            for i in range(len(category)):
                id_1 = category[i].question_category_id[0:2]
                if id_1 not in ste_1:
                    id_2 = category[i].question_category_id[2:]
                    name_1 = category[i].question_category_name[:-2]
                    dit = {"id": id_1,
                           "name": name_1,
                           "list": [
                               {
                                   "id": "01",
                                   "name": "新培",
                                   "list": []
                               },
                               {
                                   "id": "02",
                                   "name": "复审",
                                   "list": []
                               },
                           ]
                           }
                    test_paper_list = T_test_paper.objects.filter(test_paper_id__startswith=
                                                                  id_1).all()
                    # print(test_paper_list[0].test_paper_id)
                    for i in range(len(test_paper_list)):
                        test_paper_id = test_paper_list[i].test_paper_id
                        test_paper_name = test_paper_list[i].test_paper_id_name
                        temp = {
                            "id": test_paper_id,
                            "name": test_paper_name,
                            "list": [
                                {
                                    "id": "01",
                                    "name": "新培",
                                    "list": []
                                },
                                {
                                    "id": "02",
                                    "name": "复审",
                                    "list": []
                                },
                            ]
                        }
                        # print(test_paper_id)
                        # print(test_paper_name)
                        teps = test_paper_id[2:4]
                        if teps == "01":
                            dit["list"][0]["list"].append(temp)
                        else:
                            dit["list"][1]["list"].append(temp)
                    # print(dit)
                    if len(test_paper_list) != 0:
                        result.append(dit)
                    else:
                        pass
                    # print(result)
                    ste_1.add(id_1)
                else:
                    pass
            # results = json.dumps(result)
            print(result)
            return HttpResponse(result)
            # return JsonResponse(results,safe=False)
        else:
            return HttpResponse("该用户未购买任何题库")
    else:
        return HttpResponse("请求方式错误")