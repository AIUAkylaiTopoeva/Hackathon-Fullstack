from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model


User = get_user_model()

class Product(models.Model):
    title = models.CharField(max_length=120, unique=True, verbose_name='Название продукта')
    slug = models.SlugField(max_length=120, unique=True, blank=True, primary_key=True)
    description = models.TextField(verbose_name='Описание продукта',blank=True)
    image = models.ImageField(upload_to='images/', blank=True, verbose_name= 'Изображение продукта')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name= 'Цена продукта')
    in_stock = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kvargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

class Order(models.Model):
    author = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='OrderItem')
    total_sum = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    STATUSES = [
        ('D', 'Delivered'),
        ('ND', 'Not Delivered')
    ]
    status = models.CharField(max_length=2, choices=STATUSES)
    PAYMENTS = [
        ('Card', 'Card'),
        ('Cash', 'Cash')
    ]
    payment = models.CharField(max_length=4, choices=PAYMENTS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Product ID: {self.pk}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_item')
    quantity = models.PositiveIntegerField(default=1)
