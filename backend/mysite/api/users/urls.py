from django.urls import include, path
from djoser.views import TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import (ListrAllUserViewSet, CustomTokenCreateView,
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
router_v1.register(r'users/(?P<user_id>\d+)/', ListrAllUserViewSet, basename='user')
router_v1.register(r'users', ListrAllUserViewSet, basename='users')
urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/token/login/', CustomTokenCreateView.as_view()),
    path('auth/token/logout/', TokenDestroyView.as_view()),
]
