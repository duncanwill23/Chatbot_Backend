from django.urls import path
from .views import send_message
from .views import get_doctors
from .views import chatbot_view
from .views import get_provider

urlpatterns = [
    path('message/', send_message),
    path('doctor/', get_doctors),
    path('chatbot/', chatbot_view),
    path('provider/', get_provider)
]