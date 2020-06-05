from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .views import *

urlpatterns = [  
      re_path(r'send_bot_message/$',send_bot_message,
            name='send_bot_message'),         
]

