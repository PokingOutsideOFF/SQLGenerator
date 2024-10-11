from django.db import models
from django.contrib.auth.hashers import make_password
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=250)

    def set_password(self, raw_password):
        self.password = raw_password 
    
    def save(self, *args, **kwargs):
    # Hash the password before saving
        if self.password:
            self.password = make_password(self.password)  # Hash the password
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.username
