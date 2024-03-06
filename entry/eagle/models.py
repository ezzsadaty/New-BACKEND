
from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)

class Camera(models.Model):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)    

class Community(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(Person, through='UsersInCommunity')
    Community_ID = models.IntegerField(primary_key=True)

class UsersInCommunity(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    Community_ID = models.ForeignKey(Community, on_delete=models.CASCADE)
    join_date = models.DateField()

class Person_History(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    checkIn_time = models.DateTimeField()
    checkOut_time = models.DateTimeField()

class Camera_History(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    checkIn_time = models.DateTimeField()
    checkOut_time = models.DateTimeField()

class SecurityPersonnel(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True) 

class Admin(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    birth_date = models.DateField() 