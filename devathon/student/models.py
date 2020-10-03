from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pass_code = models.CharField(max_length=6, default="")
    email = models.CharField(max_length=50, default="")
    def save(self):
        super().save()

    def __str__(self):
        return self.user.username
