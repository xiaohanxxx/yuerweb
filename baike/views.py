from django.shortcuts import render

# Create your views here.

import json
from django import views
from django.shortcuts import render, HttpResponse
from . import models
from . import serializers
# Create your views here.


class BaikeArea(views.View):
    def get(self, request, *args, **kwargs):
        queryset = models.BaikeArea.objects.all()
        serializer = serializers.BaikeAreaSerializer(queryset, many=True)
        data = serializer.data
        return HttpResponse(json.dumps(data), content_type='application/json')


class BaikeArtical(views.View):
    def get(self, request, *args, **kwargs):
        parent_id = request.GET.get('p')
        queryset = models.BaikeArtical.objects.get(parent_id=parent_id)
        data = serializers.BaikeAreaSerializer(queryset).data
        return HttpResponse(json.dumps(data), content_type='application/json')
