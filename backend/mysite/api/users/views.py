from django.contrib.auth import get_user_model
from djoser.views import TokenCreateView, UserViewSet

from .serializers import MyTokenCreateSerializer

User = get_user_model()


class CustomTokenCreateView(TokenCreateView):
    serializer_class = MyTokenCreateSerializer


class CustomDjoserUserViewSet(UserViewSet):

    def get_queryset(self):
        return User.objects.all()
