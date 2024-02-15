from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
# Create your views here.

# Create your views here.


class UserLogout(APIView):
    def get(self, request):
        logout(request)
        return redirect('/user/login')
    
class UserLogin(APIView):
    def get(self, request):
        return render(request, "login.html")
    
    def post(self,request):

        data = request.data
        username = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/property/property_list')
        else:
            return render(request, "login.html")

class Landing(APIView):
    def get(self, request):

        return render(request, "index.html", {})







