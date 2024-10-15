from django.urls import path
from .views import user_login, user_signup

app_name = 'account'

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', user_signup, name='register'),
]
