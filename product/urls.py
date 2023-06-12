from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrderView, ProductViewSet

router = DefaultRouter()
router.register('orders', OrderView)
router.register('products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls))
]