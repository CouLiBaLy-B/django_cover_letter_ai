from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.user_login, name='login'),
    path('signup', views.user_signup, name='signup'),
    path('logout', views.user_logout, name='logout'),
    path('generate-cover', views.generate_cover, name="generate-cover"),
    path('cover-list', views.cover_list, name="cover-list"),
    path('cover-details/<int:pk>/', views.cover_details, name="cover-details"),
]
