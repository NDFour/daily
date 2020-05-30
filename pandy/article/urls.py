# -*- coding:utf-8 -*-
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-07-20 00:59:50
# Last Modified: 2018-09-02 14:11:27
#

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='article_index'),
    # path('pages/<str:page_num>/', views.index_by_page, name='book_index_by_page'),
    path('<int:article_id>/', views.article_detail, name='article_detail'),
]
