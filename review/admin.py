from django.contrib import admin

from .models import Comment,Like,Rating,Favorite

admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Rating)
admin.site.register(Favorite)
