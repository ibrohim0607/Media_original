from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey


class MyUser(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
