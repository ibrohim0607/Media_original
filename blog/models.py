from django.db import models
from django.contrib.auth.models import User

from authentication.models import MyUser


class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='post/')
    like = models.ManyToManyField(MyUser, related_name='like', blank=True)
    follow = models.ManyToManyField(MyUser, related_name='follow', blank=True)

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def number_of_likes(self):
        return self.like.count()

    def number_of_follows(self):
        return self.follow.count()

    def __str__(self):
        return f"{self.author.user.username}"

    @classmethod
    def all_(cls):
        query = "SELECT * FROM"
        return cls.objects.all(raw_query=query)


class Comment(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='author_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')

    message = models.CharField(max_length=250)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.user.username}'s comment"


class Like(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='liked_from')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_to')

    created_at = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    follower = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='following')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.follower.user.username
