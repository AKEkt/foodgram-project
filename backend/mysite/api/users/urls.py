from django.urls import path, include
from .views import UsersViewSet
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()

router_v1.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    # path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
