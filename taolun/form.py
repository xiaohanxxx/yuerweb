#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django import forms
from . import models


class PostingForm(forms.Form):
    title = forms.fields.CharField(
        max_length=255,
        error_messages={'required': "内容不能为空", 'max_length': "长度大于255"}
    )
    content = forms.fields.CharField(
        max_length=255,
        error_messages={'required': "内容不能为空", 'max_length': "长度大于255"}
    )

