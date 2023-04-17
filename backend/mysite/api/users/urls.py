from django.urls import include, path
from djoser.views import TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import (CustomTokenCreateView, CustomUsersViewSet, FollowViewSet,
                    ListSubscripViewSet)

router_v1 = DefaultRouter()

router_v1.register(r'users', CustomUsersViewSet, basename='users')

urlpatterns = [

    path('users/me/', CustomUsersViewSet.as_view({'get': 'me'})),
    # path('users/<int:pk>/', CustomUsersViewSet.as_view({'get': 'retrieve'})),
    path('users/subscriptions/', ListSubscripViewSet.as_view({'get': 'list'})),
    path('users/<int:pk>/subscribe/', FollowViewSet.as_view()),
    path('auth/token/login/', CustomTokenCreateView.as_view()),
    path('auth/token/logout/', TokenDestroyView.as_view()),
    path('', include(router_v1.urls)),

]
