from django.urls import path
from authentication.views import *

urlpatterns = [
    path('logout/', logoutView, name='logout'),
    path('loginuser', loginUserView, name="loginUser"),
    path('registeruser', registerUserView, name="registerUser"),
]