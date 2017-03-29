__author__ = "Harshit"

from django.conf.urls import url, include
from rest_framework import routers
from django.views.generic import TemplateView
import apiviews
import views

urlpatterns = [

    url(r'^compiler$', TemplateView.as_view(template_name='Compiler/compiler_try.html')),
    url(r'^progList$',views.ProgramListView.as_view(), name='progs_list'),
    url(r'^progList/(?P<pk>[0-9]+)$',views.ProgramDetailView.as_view()),
    url(r'^addProg$',views.ProgramCreate.as_view()),
    url(r'^results',TemplateView.as_view(template_name='Compiler/results.html')),
    url(r'^progList/time/(?P<pk>[0-9]+)$',apiviews.getTimer),
    url(r'^api/start/(?P<pk>[0-9]+)$', apiviews.startTimer),
    url(r'^api/compile', apiviews.compile),
    url(r'^api/run', apiviews.run),
    url(r'^api/submit',apiviews.submit),
    url(r'^api/results',apiviews.results),

]