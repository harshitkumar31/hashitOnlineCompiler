__author__ = "Harshit"

from django.contrib import admin
from models import *
from forms import *

# admin.site.register(Problem)
admin.site.register(Solution)
admin.site.register(Tests)
admin.site.register(Problem, Cab_Admin)