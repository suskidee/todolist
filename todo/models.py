from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class New(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user}'s todo item"
