from django.urls import include, path
from djoser.views import TokenDestroyView
from rest_framework.routers import DefaultRouter
from .views import (CustomUsersViewSet, CustomTokenCreateView,
                    ListSubscripViewSet, FollowViewSet)

router_v1 = DefaultRouter()
router_v1.register(
    r'users/subscriptions',
    ListSubscripViewSet, basename='subscriptions'
    )
router_v1.register(r'users', CustomUsersViewSet, basename='users')
urlpatterns = [
    path('users/<int:pk>/subscribe/', FollowViewSet.as_view()),
    path('auth/token/login/', CustomTokenCreateView.as_view()),
    path('auth/token/logout/', TokenDestroyView.as_view()),
    path('', include(router_v1.urls)),
]
