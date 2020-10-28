from django.urls import path, re_path
from hospital import views
from django.conf.urls import url

from .views import Area, Artical

urlpatterns = [
    path(r'area/', Area.as_view()),
    re_path(r'artical/', Artical.as_view()),
]