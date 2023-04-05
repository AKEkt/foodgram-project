from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import TokenCreateView, UserViewSet
from rest_framework import viewsets
from .serializers import (ListSubscripSerializer, MyDjoserUserSerializer,
                          MyTokenCreateSerializer, SubscripUserSerializer)
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Follow
from rest_framework import generics
User = get_user_model()


class CustomTokenCreateView(TokenCreateView):
    serializer_class = MyTokenCreateSerializer


class CustomUsersViewSet(UserViewSet):
    serializer_class = MyDjoserUserSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if self.action == 'list':
            return queryset
        return queryset.filter(pk=user.pk)


class ListSubscripViewSet(UserViewSet):
    serializer_class = ListSubscripSerializer

    def get_queryset(self):
        return User.objects.filter(
           following__user=self.request.user
        )


class FollowViewSet(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = SubscripUserSerializer
    queryset = Follow.objects.all()
    http_method_names = ['post', 'delete']

    def perform_create(self, serializer):
        author = get_object_or_404(User,
                                   id=self.kwargs.get('pk'))
        serializer.save(user=self.request.user, author=author)
    
    def delete(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('pk'))
        follow_user = Follow.objects.filter(user=self.request.user, author=author)
        if follow_user.exists():
            follow_user.delete()
            return Response(
                {
                    'выполнено': 'Успешная отписка'
                }, status=status.HTTP_204_NO_CONTENT)
        return Response(
            {
                'ошибка': 'Объект не найден'
            }, status=status.HTTP_400_BAD_REQUEST)
