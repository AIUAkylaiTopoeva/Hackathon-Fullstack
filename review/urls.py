from django.urls import path, include
from .views import CommentViewSet, RatingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('comments', CommentViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]