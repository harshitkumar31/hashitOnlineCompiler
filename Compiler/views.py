__author__ = "Harshit"

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from Compiler.models import  *
from django import forms
from django.forms.extras.widgets import SelectDateWidget

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@method_decorator(login_required, name='dispatch')
class ProgramListView(ListView):
    model = Problem
    context_object_name = 'progs'

@method_decorator(login_required, name='dispatch')
class ProgramCreate(CreateView):
    model = Problem
    fields = ['title','description','difficulty']

    def get_success_url(self):
        return reverse('progs_list')

@method_decorator(login_required, name='dispatch')
class ProgramDetailView(DetailView):
    model = Problem
    context_object_name = 'problem'