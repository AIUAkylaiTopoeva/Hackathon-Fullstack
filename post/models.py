from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=120,unique=True,verbose_name='Название категории')
    slug = models.SlugField(max_length=125, unique=True,blank=True,primary_key=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts',verbose_name='Автор')
    title = models.CharField(max_length=120)
    body = models.TextField()
    image = models.ImageField(upload_to='posts/',blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.title}'
    


