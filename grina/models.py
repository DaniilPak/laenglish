from distutils.command.upload import upload
from email.mime import image
from operator import mod
from pyexpat import model
from secrets import choice
from xmlrpc.client import Server
from django.db import models
# AUTH MODEL 
from django.contrib.auth.models import User

# Create your models here.

# Sections & Courses & SubCourses

class SubCourse(models.Model):
    id = models.AutoField(primary_key=True)
    subcourse_title = models.CharField(max_length=100)
    api_link = models.URLField()

class Data(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    img_uri = models.URLField()
    sub_courses = models.ManyToManyField(SubCourse)

class Course(models.Model):
    section = models.CharField(max_length=100)
    data = models.ManyToManyField(Data, blank=True)
    
# VideoObject that contains all data
# we need to create a full course

# Server choice is a part of VideoTest type component
# It give 4 choice buttons with 1 right answer

class ServerChoice(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField()

# Data from which we will craft 
# a course
class VideoObject(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.FileField(upload_to='grinavideos')
    tip = models.CharField(max_length=200)
    eng_text = models.CharField(max_length=200)
    ru_text = models.CharField(max_length=200)
    server_choice_1 = models.ForeignKey(ServerChoice, on_delete=models.CASCADE, related_name='sc1')
    server_choice_2 = models.ForeignKey(ServerChoice, on_delete=models.CASCADE, related_name='sc2')
    server_choice_3 = models.ForeignKey(ServerChoice, on_delete=models.CASCADE, related_name='sc3')
    server_choice_4 = models.ForeignKey(ServerChoice, on_delete=models.CASCADE, related_name='sc4')

    def __str__(self) -> str:
        return '%s' % (self.id)

# Stack Of VideoObject
# we will get JSON data from this object
class CraftStack(models.Model):
    
    id = models.AutoField(primary_key=True)
    video_objects = models.ManyToManyField(VideoObject, blank=True)

    def __str__(self) -> str:
        return '%s' % (self.id)