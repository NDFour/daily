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
    path('', views.book_index, name='book_index'),
    path('pages/<str:page_num>/', views.index_by_page, name='book_index_by_page'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('category/', views.book_category, name='book_category'),
    # 通过构造 URL 实现搜索
    # path('search/<str:movie_name>', views.movie_search, name='movie_search'),
    # navbar 中的 Form 搜索
    path('search/', views.book_search_navbar, name='book_search_navbar'),
    # 热搜榜
    path('resou/', views.book_resou, name='book_resou'),
    # 热搜榜 json format
    path('resou_json/', views.book_resou_json, name='book_resou_json'),
    # 八百里加急 立即催
    path('babaili_jiaji/', views.babaili_jiaji, name='babaili_jiaji'),
    path('invalid_url_report/', views.invalid_url_report, name='invalid_url_report'),
]
