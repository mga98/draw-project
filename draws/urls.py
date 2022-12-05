from django.urls import path

from . import views

app_name = 'draws'

urlpatterns = [
    path('', views.home, name='home'),
    path('draw/<int:pk>/', views.draw, name='draw_view'),
]
