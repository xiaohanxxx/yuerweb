from django import views
from django.shortcuts import render, HttpResponse

# Create your views here.


class Login(views.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("is a test_django")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        return HttpResponse("your method post" + "  " + username + "  " + password)
