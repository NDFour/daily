# -*- coding:utf-8 -*-
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2019-02-26 14:44:30
# Last Modified: 2019-02-27 15:19:28
#

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='manager_index'),
    path('dormitory/<int:dormitory_number>/', views.dormitory_detail, name='dormitory_detail'),
    path('student/<int:stu_number>/', views.student_detail, name='student_detail'),
]
