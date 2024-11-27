from App import views
from django.urls import path

urlpatterns = [
    path('register/', views.user_registration, name='register'),
    
    path('login/', views.login, name='username'),
    path('logout/',views.logout,name='logout'),
]