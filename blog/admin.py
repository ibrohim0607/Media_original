from django.contrib import admin
from blog.models import Post, Comment, Follow, Like, Settings

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Settings)