
from django.urls import path
from webhook import views

urlpatterns = [
   
    path('webhook/', views.webhook, name='webhook'),
    path('', views.chat_view, name='chat_view'),
    
    path('chat/', views.chat_view, name='chat_view'),

    path('phone-numbers/', views.get_phone_numbers, name='get_phone_numbers'),
    path('messages/<str:phone_number>/', views.get_messages_by_phone, name='get_messages_by_phone'),
    

]