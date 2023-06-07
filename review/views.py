from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from .serializers import CommentSerializer, RatingSerializer
from .models import Comment, Rating, Like
from .permissions import IsAuthorOrReadOnly
from .serializers import LikeSerializer
from post.models import Post

class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorOrReadOnly]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        comment = self.get_object()
        post = comment.post  # Получаем связанный с комментарием пост
        author = request.user
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                like = Like.objects.get(post=post, comment=comment, author=author)  # Используем поле "comment" вместо "comments"
                like.delete()
                message = 'disliked'
            except Like.DoesNotExist:
                Like.objects.create(post=post, comment=comment, author=author)  # Используем поле "comment" вместо "comments"
                message = 'liked'
            return Response(message, status=200)
    

class RatingViewSet(PermissionMixin ,ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

