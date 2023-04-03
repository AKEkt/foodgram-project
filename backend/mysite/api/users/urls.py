from django.urls import path, include
from .views import CustomTokenCreateView, CustomDjoserUserViewSet
from djoser.views import TokenDestroyView
from rest_framework.routers import DefaultRouter


router_v1 = DefaultRouter()
router_v1.register(r'users', CustomDjoserUserViewSet, basename='users')
router_v1.register(r'tags', CustomDjoserUserViewSet, basename='tags')
urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/token/login/', CustomTokenCreateView.as_view()),
    path('auth/token/logout/', TokenDestroyView.as_view()),
]
