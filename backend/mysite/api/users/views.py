from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import TokenCreateView, UserViewSet
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers.serializers import MyDjoserUserSerializer
from .models import Follow
from .serializers import MyTokenCreateSerializer, SubscripUserSerializer

User = get_user_model()


class CustomTokenCreateView(TokenCreateView):
    serializer_class = MyTokenCreateSerializer


class CustomUsersViewSet(UserViewSet):
    serializer_class = MyDjoserUserSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return User.objects.all()

    @action(
        detail=False,
        methods=('get',), permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class ListSubscripViewSet(UserViewSet):
    serializer_class = SubscripUserSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)


class FollowViewSet(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = SubscripUserSerializer
    queryset = Follow.objects.all()
    http_method_names = ['post', 'delete']

    def create(self, request, *args, **kwargs):
        author = get_object_or_404(User,
                                   id=self.kwargs.get('pk'))
        user = self.request.user
        if user == author:
            return Response(
                {
                    'ошибка': 'Нельзя подписаться на себя!'
                }, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user, author=author).exists():
            return Response(
                {
                    'ошибка': 'Нельзя подписаться на одного автора повторно!'
                }, status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.create(user=user, author=author)
        serializer = self.get_serializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('pk'))
        follow_user = Follow.objects.filter(user=self.request.user,
                                            author=author)
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
