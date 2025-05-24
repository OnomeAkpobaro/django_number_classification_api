from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NumberClassificationViewset

router = DefaultRouter()
router.register(r'numbers', NumberClassificationViewset, basename='numbers')

urlpatterns = [
    path('', include(router.urls)),
    
]