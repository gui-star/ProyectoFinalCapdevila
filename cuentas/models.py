from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    description = models.TextField()
    website = models.URLField()
    nombre = models.CharField(max_length=100) 

    def __str__(self):
        return self.user.username
