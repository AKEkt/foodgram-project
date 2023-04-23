from django.urls import include, path
from djoser.views import TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import (CustomTokenCreateView, CustomUsersViewSet, FollowViewSet,
                    ListSubscripViewSet)

router = DefaultRouter()

router.register(r'', CustomUsersViewSet, basename='users')

urlpatterns = [

    path('me/', CustomUsersViewSet.as_view({'get': 'me'})),
    path('<int:pk>/', CustomUsersViewSet.as_view({'get': 'retrieve'})),
    path('subscriptions/', ListSubscripViewSet.as_view({'get': 'list'})),
    path('<int:pk>/subscribe/', FollowViewSet.as_view()),
    path('token/login/', CustomTokenCreateView.as_view()),
    path('token/logout/', TokenDestroyView.as_view()),
    path('', include(router.urls)),

]
