# -*- coding:utf-8 -*-
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-07-20 00:59:50
# Last Modified: 2018-07-23 18:01:41
#

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movie_index'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('search/<str:movie_name>', views.movie_search, name='movie_search'),
]
