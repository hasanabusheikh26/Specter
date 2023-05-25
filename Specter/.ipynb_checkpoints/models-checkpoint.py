from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#a model to create a Database for our model in the chat


class Past(models.Model):
    user = models.ForeignKey(User, related_name="code", on_delete=models.DO_NOTHING)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    
    def __str__(self):
        return self.question  # Create your models here.
