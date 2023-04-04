from django.urls import include, path
from djoser.views import TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import (CustomDjoserUserViewSet, CustomTokenCreateView,
                    ListSubscripViewSet, FollowViewSet)

router_v1 = DefaultRouter()
router_v1.register(
    r'users/(?P<subs_id>\d+)/subscribe',
    FollowViewSet, basename='subscribe'
    )
router_v1.register(
    r'users/subscriptions',
    ListSubscripViewSet, basename='subscriptions'
    )
router_v1.register(r'users', CustomDjoserUserViewSet, basename='users')
router_v1.register(r'tags', CustomDjoserUserViewSet, basename='tags')
urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/token/login/', CustomTokenCreateView.as_view()),
    path('auth/token/logout/', TokenDestroyView.as_view()),
]
