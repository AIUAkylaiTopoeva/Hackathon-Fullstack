from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.crypto import get_random_string

class UserManager(BaseUserManager):
    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Поле не может быть пустым')
        email = self.normalize_email(email)
        user = self.model(email= email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save()
        return user
    
    def create_user(self, email, password,**extra_fields):
        return self._create(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fieldes):
        extra_fieldes.setdefault('is_staff', True)
        extra_fieldes.setdefault('is_active', True) 
        extra_fieldes.setdefault('is_superuser', True) 
        return self._create(email, password, **extra_fieldes) 
    

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20,blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=20, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []     #обязательные поля для суперпользователя

    def __str__(self) -> str:
        return f'{self.id} -> {self.email}'
    
    def has_module_perms(self, app_label):     #проверяет есть ли пермишн на какой-либо объект
        return self.is_staff
    
    def has_perm(self, perm, obj=None):
        return self.is_staff
    
    def create_activation_code(self):       #отправляется код для активации
        code = get_random_string(10, allowed_chars='1234567890!@#$%^&*()_')
        self.activation_code = code
        