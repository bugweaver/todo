from django.db import models
from django.contrib.auth.models import User

class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Task(models.Model):
    list_name = models.ForeignKey(List, related_name='tasks' ,on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text
