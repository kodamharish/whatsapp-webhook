
from django.urls import path
from webhook import views

urlpatterns = [
   
    path('webhook/', views.webhook, name='webhook'),
    path('', views.home, name='home'),
]