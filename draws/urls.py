from django.urls import path

from . import views

app_name = 'draws'

urlpatterns = [
    path('', views.home, name='home'),
    path('draws/<int:pk>/', views.draw, name='draw_view'),
    path('draws/all/', views.all_draws, name='all_draws'),
    path('draws/search/', views.DrawSearch.as_view(), name='draws_search'),
]
