from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import Comment, Rating, Like, Favorites

class CommentSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        comment = Comment.objects.create(author=user, **validated_data)
        return comment

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes_count'] = instance.likes.count()
        return representation

class RatingSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = '__all__'

class LikeSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Like
        fields = '__all__'
    
class FavoriteSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    post = ReadOnlyField()

    class Meta:
        model = Favorites
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        favorite = Favorites.objects.create(author = user, **validated_data)
        return favorite