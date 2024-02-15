from django.urls import path
from .views import *

app_name = 'user_model'

urlpatterns = [
    # path('user_check/', views.UserCheck.as_view(), name='user_check'),
    path('login',UserLogin.as_view(), name='login'),
    path('landing', Landing.as_view(), name='landing'),
    path('logout', UserLogout.as_view(), name='logout'),

]