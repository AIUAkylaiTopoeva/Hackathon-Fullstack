from django.db import models
from post.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    body = models.CharField(max_length=250)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    is_liked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.post} liked by {self.author.username}'
    
class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings', verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', verbose_name='Автор')
    rating = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return f'{self.rating}'
    
class Favorite(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    
    def __str__(self):
        return f'{self.post.title} favorites by {self.author.username}'
