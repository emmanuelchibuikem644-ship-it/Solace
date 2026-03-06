from django.urls import path
from .views import register,  chatbot_response
urlpatterns = [
    path("register/", register),
    path("chat/", chatbot_response, name="chatbot"),
]

    