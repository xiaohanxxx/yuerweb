from django.urls import path, re_path
from hospital import views
from django.conf.urls import url


urlpatterns = [
    path('', views.hospital),

]