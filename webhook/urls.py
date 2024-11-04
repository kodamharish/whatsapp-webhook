
from django.urls import path
from .views import *

urlpatterns = [
   
    path('webhook/', webhook, name='webhook'),
    path('', chat_view, name='chat_view'),
    
    path('chat/', chat_view, name='chat_view'),

    path('phone-numbers/', get_phone_numbers, name='get_phone_numbers'),
    path('messages/<str:phone_number>/', get_messages_by_phone, name='get_messages_by_phone'),
    

]