from django.urls import include, path
from recipes.views import IngredientsViewSet, TagsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
urlpatterns = [

    path('', include(router.urls)),
    path('recipes/', include('recipes.urls')),
    path('users/', include('users.urls')),
    path('auth/', include('users.urls')),

]
