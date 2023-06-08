from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser,AllowAny
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator   


from .serializers import CategorySerializer,PostSerialiser
from .models import Category, Post
from .permissions import IsAdminOrActivePermission, IsOwnerPermission

from review.serializers import LikeSerializer, FavoriteSerializer
from review.models import Like, Favorites

class PermissionMixin:
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAdminUser]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerialiser

    @method_decorator(cache_page(60))
    def list(self,request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['title','created_at']
    ordering_fields = ['created_at', 'title']

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [IsOwnerPermission]
        elif self.action == 'create':
            self.permission_classes = [IsAdminOrActivePermission]
        elif self.action in ['list', 'retrive']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    
    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        author = request.user
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                like = Like.objects.get(post=post, author=author)
                like.delete()
                message  = 'disliked'
            except Like.DoesNotExist:
                Like.objects.create(post=post, author=author)
                message = 'liked'
            return Response(message, status=200)

    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk=None):
        post = self.get_object()
        author = request.user
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                favorite = Favorites.objects.get(post=post, author=author)
                favorite.delete()
                message  = 'delete from favorites'
            except Favorites.DoesNotExist:
                Favorites.objects.create(post=post, author=author)
                message = 'favorites to saved'
            return Response(message, status=200)
