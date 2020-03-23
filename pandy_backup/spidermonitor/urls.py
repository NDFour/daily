# -*- coding:utf-8 -*-
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-07-20 00:59:50
# Last Modified: 2018-08-22 09:55:00
#

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='spidermonitor_index'),
    path('get/<int:maxid>', views.get, name='spidermonitor_get'),
    path('detail/<int:infoid>', views.detail, name='spidermonitor_detail'),
]
