"""Examination_App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import Examination_App.views as views
import User.views as User_view
import Examination.views as Examination_view
from django.urls import path
urlpatterns = [
    path('',views.index),
    path('register/',User_view.register),
    path('login/',User_view.login),
    path('log_out/',User_view.log_out),
    path('purchase/',User_view.purchase),
    path('get_all_testpaper/',Examination_view.get_all_testpaper),
    path('get_user_test_no/',Examination_view.get_user_test_no)
]
