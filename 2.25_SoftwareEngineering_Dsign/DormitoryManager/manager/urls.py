# -*- coding:utf-8 -*-
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2019-02-26 14:44:30
# Last Modified: 2019-02-26 14:45:14
#

from django.urls import path
from . import views

urlpatterns = {
    path('', views.index, name='manager_index'),
}
