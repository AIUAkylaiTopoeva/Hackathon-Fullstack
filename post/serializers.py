from rest_framework import serializers
from django.db.models import Avg
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Post

from review.models import Like, Comment, Rating, Favorites
from review.serializers import LikeSerializer, RatingSerializer, FavoriteSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostSerialiser(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source ='author.name')

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        author = Post.objects.create(author=user, **validated_data)
        return author


    def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['likes_count'] = instance.likes.count()
            representation['comments'] = [i.body for i in instance.comments.all()]
            representation['rating'] = instance.ratings.aggregate(Avg('rating'))
            ['rating__avg']

            return representation