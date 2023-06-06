from rest_framework.serializers import ModelSerializer, ValidationError, ReadOnlyField
from .models import Comment, Rating, Like, Favorites

class CommentSerializer(ModelSerializer):
    author = ReadOnlyField(source = 'author.email')

    class Meta:
        model = Comment
        fields = '__all__'
    
    def create(self, validated_data):
        user = self.context.get('request').user
        comment = Comment.objects.create(author = user, **validated_data)  # create не нужно сохронять, автомотически сохраняется. Обязательно нужно return
        return comment
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes_count'] = instance.likes.count()
        return representation

class RatingSerializer(ModelSerializer):
    author = ReadOnlyField(source = 'author.email')
    class Meta:
        model = Rating
        fields = '__all__'
    
    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise ValidationError('rating must be in range 1-5')
        return rating
    
    def validate_product(self, post):
        if self.Meta.model.objects.filter(post=post).exists():
            raise ValidationError(
                'Рейтинг уже поставлен'
            )
        return post
    
    def create(self, validated_data):
        user = self.context.get('request').user
        rating = Rating.objects.create(author= user, **validated_data)
        return rating

class LikeSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    post= ReadOnlyField()

    class Meta:
        model = Like
        fields = '__all__'
    
    def create(self, validated_data):
        user = self.context.get('request').user
        like= Like.objects.create(author = user, **validated_data)
        return like
    
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