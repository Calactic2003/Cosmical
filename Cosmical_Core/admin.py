from django.contrib import admin
from .models import Profile, Post, LikePost, Comment, FollowersCount, ThreadModel, Notification

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Comment)
admin.site.register(FollowersCount)
admin.site.register(ThreadModel)
admin.site.register(Notification)
