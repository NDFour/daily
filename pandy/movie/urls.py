# -*- coding:utf-8 -*-
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-07-20 00:59:50
# Last Modified: 2018-08-10 18:21:00
#

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movie_index'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('search/<str:movie_name>', views.movie_search, name='movie_search'),
    path('confirm_invalid/<int:movie_id>/<int:urlstate>', views.confirm_invalid, name='cofirm_invalid'),
    path('invalid_url_report/<int:movie_id>/<int:urlstate>', views.invalid_url_report, name='invalid_url_report'),
]
