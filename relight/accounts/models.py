from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = CloudinaryField('image', resource_type='auto', default='default_profile_picture.jpg', blank=True, null=True)

    #Function to save default profile picture
    def save(self, *args, **kwargs):
        if not self.profile_picture:
            self.profile_picture = 'default_profile_picture.jpg'
        super(Profile, self).save(*args, **kwargs)