from rest_framework import serializers
from django.db.models import Avg

from .models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostSerialiser(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source ='author.name')

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes_count'] = instance.likes.count()
        representation['comments'] = [i.body for i in instance.comments.all()]
        representation['rating'] = instance.ratings.aggregate(Avg('rating'))
        ['rating_avg']

        return representation