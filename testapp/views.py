from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django import views


class Login(views.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("is a test_django")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        return HttpResponse("your method post" + "  " + username + "  " + password)
