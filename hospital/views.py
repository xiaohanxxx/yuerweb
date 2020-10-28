import json
from django import views
from django.shortcuts import render, HttpResponse
from . import models
from . import serializers
# Create your views here.


class Area(views.View):
    def get(self, request, *args, **kwargs):
        queryset = models.Area.objects.all()
        serializer = serializers.AreaSerializer(queryset, many=True)
        data = serializer.data
        return HttpResponse(json.dumps(data), content_type='application/json')


class Artical(views.View):
    def get(self, request, *args, **kwargs):
        parent_id = request.GET.get('p')
        queryset = models.Artical.objects.get(parent_id=parent_id)
        data = serializers.ArticalSerializer(queryset).data
        return HttpResponse(json.dumps(data), content_type='application/json')
