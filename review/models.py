from django.db import models
from django.contrib.auth import get_user_model
from post.models import Post

User = get_user_model()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    body = models.CharField(max_length=250)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body

class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings', verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', verbose_name='Автор')
    rating = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return self.rating
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    def __str__(self) -> str:
        return f'liked by {self.author.email}'


class Favorites(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    
    def __str__(self):
        return f'{self.post.title} favorites by {self.author.name}'