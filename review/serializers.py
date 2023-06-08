from rest_framework.serializers import ModelSerializer, ValidationError, ReadOnlyField
from .models import Comment,Like,Rating,Favorite

class LikeSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')
    post= ReadOnlyField()

    class Meta:
        model = Like
        fields = '__all__'
    
    def create(self, validated_data):
        user = self.context.get('request').user
        like= Like.objects.create(author = user, **validated_data)
        return like
    
class CommentSerializer(ModelSerializer):
    author = ReadOnlyField(source = 'author.username')

    class Meta:
        model = Comment
        fields = '__all__'
    
    def create(self, validated_data):
        user = self.context.get('request').user
        comment = Comment.objects.create(author = user, **validated_data)  # create не нужно сохронять, автомотически сохраняется. Обязательно нужно return
        return comment
    
    
    
class RatingSerializer(ModelSerializer):
    author = ReadOnlyField(source = 'author.username')
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
    
class FavoriteSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')
    post = ReadOnlyField()

    class Meta:
        model = Favorite
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        favorite = Favorite.objects.create(author = user, **validated_data)
        return favorite