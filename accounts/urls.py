from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('mydraws/', views.my_draws, name='my_draws'),
    path('mydraws/<int:pk>/edit/', views.my_draws_edit, name='my_draws_edit'),
    path('mydraws/create/', views.my_draws_create, name='my_draws_create'),
    path('mydraws/delete/', views.my_draws_delete, name='my_draws_delete'),
    path('profile/<int:pk>/', views.profile_view, name='profile_view'),
    path('profile/<int:pk>/edit/', views.profile_edit, name='profile_edit'),
    path('like/', views.like_unlike, name='like_unlike'),
    path('liked/', views.liked_posts, name='liked_posts'),
]
