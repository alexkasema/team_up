from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#! room is a child of a topic
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name 

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) #!null is for database, blank is for form submission
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True) #! for every time we update the room
    created = models.DateTimeField(auto_now_add=True) #! only updates when a room is created

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #! one to many relationship (a user can have many messages but a message can only have one user)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) #! for every time we update the room
    created = models.DateTimeField(auto_now_add=True) #! only updates when a room is created

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return self.body[0:50]
