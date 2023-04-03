from django.contrib.auth import get_user_model
from djoser.views import TokenCreateView, UserViewSet

from .serializers import MyTokenCreateSerializer, MyDjoserUserSerializer

User = get_user_model()


class CustomTokenCreateView(TokenCreateView):
    serializer_class = MyTokenCreateSerializer


class CustomDjoserUserViewSet(UserViewSet):
    serializer_class = MyDjoserUserSerializer

    def get_queryset(self):
        return User.objects.all()
