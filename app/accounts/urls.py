from django.urls import path, include
from . import views 

app_name = 'accounts'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('', include('django.contrib.auth.urls')),	
]   

