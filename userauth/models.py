<<<<<<< HEAD
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField(primary_key=True,default=0)
    bio = models.TextField(blank=True,default="")
    profileimg = models.ImageField(upload_to='profile_image',default='')
    location = models.CharField ( max_length=100, blank=True,default="")


    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    create_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
=======
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Profile(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile', unique=True)
    id_user     = models.IntegerField(default=0)
    bio         = models.TextField(blank=True, default='')
    profileimg  = models.ImageField(
        upload_to='profile_images',
        default='blank-profile-picture.png',
    )
    location    = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name        = 'Profile'
        verbose_name_plural = 'Profiles'


class Post(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user        = models.CharField(max_length=150)
    image       = models.ImageField(upload_to='post_images')
    caption     = models.TextField(blank=True, default='')
    created_at  = models.DateTimeField(default=timezone.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} — {str(self.id)[:8]}'

    class Meta:
        ordering            = ['-created_at']
        verbose_name        = 'Post'
        verbose_name_plural = 'Posts'


class LikePost(models.Model):
    post_id  = models.CharField(max_length=500)
    username = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.username} liked {self.post_id[:8]}'

    class Meta:
        # Prevent duplicate likes at the DB level
        unique_together     = ('post_id', 'username')
        verbose_name        = 'Like'
        verbose_name_plural = 'Likes'


class Followers(models.Model):
    follower = models.CharField(max_length=150)
    user     = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.follower} → {self.user}'

    class Meta:
        # Prevent duplicate follow relationships
        unique_together     = ('follower', 'user')
        verbose_name        = 'Follower'
        verbose_name_plural = 'Followers'
>>>>>>> 8e6df7d041b0b59b7b10caede3184c4b06cee6ff
