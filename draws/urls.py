from django.urls import path
from rest_framework.routers import SimpleRouter

from . import api, views

app_name = 'draws'

draw_api_v2_router = SimpleRouter()
draw_api_v2_router.register(
    'draws/api/v2',
    viewset=api.DrawAPIv2ViewSet
)

urlpatterns = [
    path('', views.home, name='home'),
    path('draws/<int:pk>/', views.draw, name='draw_view'),
    path('draws/all/', views.all_draws, name='all_draws'),
    path('draws/search/', views.DrawSearch.as_view(), name='draws_search'),
    path('draws/api/v1/', views.HomeViewApi.as_view(), name='draws_api_v1'),
]

urlpatterns += draw_api_v2_router.urls
