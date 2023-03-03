from django.urls import path

from . import views
from . import api

app_name = 'draws'

urlpatterns = [
    path('', views.home, name='home'),
    path('draws/<int:pk>/', views.draw, name='draw_view'),
    path('draws/all/', views.all_draws, name='all_draws'),
    path('draws/search/', views.DrawSearch.as_view(), name='draws_search'),
    path('draws/api/v1/', views.HomeViewApi.as_view(), name='draws_api_v1'),
    path('draws/api/v2/', api.DrawAPIv2List.as_view(), name='draws_api_v2'),
    path(
        'draws/api/v2/<int:pk>/',
        api.DrawAPIv2Detail.as_view(),
        name='draws_api_v2_detail',
    ),
]
