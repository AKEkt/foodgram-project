from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import TokenCreateView, UserViewSet
from rest_framework import status, viewsets
from rest_framework.response import Response
# from rest_framework.views import APIView

from .models import Follow
from .serializers import (MyDjoserUserSerializer, MyTokenCreateSerializer,
                          ListSubscripSerializer)

User = get_user_model()


class CustomTokenCreateView(TokenCreateView):
    serializer_class = MyTokenCreateSerializer


class CustomDjoserUserViewSet(UserViewSet):
    serializer_class = MyDjoserUserSerializer

    def get_queryset(self):
        return User.objects.all()


class ListSubscripViewSet(CustomDjoserUserViewSet):
    serializer_class = ListSubscripSerializer

    def get_queryset(self):
        return User.objects.filter(
           following__user=self.request.user
        )


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = SubscripUserSerializer

    def perform_create(self, serializer):
        author = get_object_or_404(User,
                                   id=self.kwargs.get('subs_id'))
        serializer.save(user=self.request.user, author=author)
