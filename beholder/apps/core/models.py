from django.db import models

# Create your models here.
class Person(models.Model):
    login = models.TextField(max_length=30, unique=True)
    name = models.TextField(max_length=80)
    profile_picture = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.login

class Post(models.Model):
    id = models.TextField(max_length=255, primary_key=True, unique=True)
    author = models.ForeignKey(Person)
    dateOfCreation = models.DateTimeField()
    photo = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    network = models.CharField(max_length=255) # E.g. Twitter / Instagram

    def __str__(self):
        return self.author.login

class Tag(models.Model):
    post = models.ManyToManyField(Post)
    tag = models.CharField(max_length=255)

class Connection(models.Model):
    post = models.ForeignKey(Post)
    user = models.ManyToManyField(Person)
    text = models.TextField(max_length=255, blank=True, null=True)
    type = models.IntegerField(default=0)

class Place(models.Model):
    id = models.TextField(max_length=255, primary_key=True, unique=True)
    name = models.TextField(max_length=80)
    checkins = models.IntegerField()

class Tip(models.Model):
    id = models.TextField(max_length=255, primary_key=True, unique=True)
    author = models.ForeignKey(Person)
    place = models.ForeignKey(Place)
    text = models.TextField(max_length=80)
    dateOfCreation = models.DateTimeField()

#class Photo(models.Model):
    #id = models.TextField(max_length=255, primary_key=True, unique=True)
    #author = models.ForeignKey(Person)
    #place = models.ForeignKey(Place)
    #photo = models.CharField(max_length=255)
    #dateOfCreation = models.DateTimeField()