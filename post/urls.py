from django.urls import path,include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings



from .views import CategoryViewSet, PostViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('posts', PostViewSet)


urlpatterns = [
    path('', include(router.urls)),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)