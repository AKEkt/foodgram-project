from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TagsViewSet, IngredientsViewSet, RecipesViewSet
router_v1 = DefaultRouter()

router_v1.register(r'tags', TagsViewSet, basename='tags')
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register(r'recipes', RecipesViewSet, basename='recipes')
urlpatterns = [

    # path('recipes/', RecipesViewSet.as_view({'get': 'list',
    #                                         'post': 'create'})),
    # path('recipes/<int:pk>/', RecipesViewSet.as_view({'get': 'retrieve'})),
    path('', include(router_v1.urls)),

]
