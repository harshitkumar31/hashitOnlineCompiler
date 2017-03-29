__author__ = "Harshit"

from django.db import models
from django.contrib.auth.models import User
import os



class Tests(models.Model):
    test_name = models.CharField(max_length=20)
    prog_input = models.CharField(max_length=1000)
    output = models.CharField(max_length=1000)

    def __str__(self):
        return self.test_name


class Problem(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    difficulty = models.CharField(max_length=20)
    tests = models.ManyToManyField(Tests)

    def __str__(self):
        return self.title


class TimerProblem(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Problem)
    # time_init = models.TimeField(auto_now_add=True)
    time_init = models.DateTimeField(auto_now_add=True)

class Solution(models.Model):
    # submission_name = models.CharField(max_length=50)

    question = models.ForeignKey(Problem)
    user = models.ForeignKey(User)
    program = models.CharField(max_length=2000)
    # output = models.CharField(max_length=1000)
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.submission_name

