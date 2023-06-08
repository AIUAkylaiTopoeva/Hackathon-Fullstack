
from .serializers import CommentSerializer, RatingSerializer
from .models import Comment, Rating
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAuthorOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Like
from .serializers import LikeSerializer


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorOrReadOnly]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]


class CommentViewSet(PermissionMixin ,ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    
class RatingViewSet(PermissionMixin ,ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
