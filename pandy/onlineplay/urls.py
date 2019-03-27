# -*- coding:utf-8 -*-
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-07-20 00:59:50
# Last Modified: 2018-09-08 17:51:06
#

from django.urls import path
from . import views

urlpatterns = [
    path('', views.onlineplay_index, name='onlineplay_index'),
    path('pages/<str:page_num>/', views.onlineplay_index_by_page, name='onlineplay_index_by_page'),
    path('<int:movie_id>/', views.onlineplay_detail, name='onlineplay_detail'),
    path('getVipByCode/<int:vipCode>/', views.getVipByCode, name='getVipByCode'),
]
