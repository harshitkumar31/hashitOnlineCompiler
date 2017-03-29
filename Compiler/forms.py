from django.contrib import admin

__author__ = "Harshit"

from django import forms
from models import *

class CabModelForm( forms.ModelForm ):
    description = forms.CharField(widget=forms.Textarea)
    # title = forms.CharField(widget=forms.TextInput)
    # difficulty = forms.CharField(widget=forms.TextInput)




    class Meta:
        fields = ['title', 'description', 'difficulty', 'tests']
        model = Problem

class Cab_Admin( admin.ModelAdmin ):
    form = CabModelForm


