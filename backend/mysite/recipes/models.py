from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

COLOR_PALETTE = [
    ("#ff9a53", "breakfast", ),
    ("#7fff7e", "lunch", ),
    ("#a796ff", "dinner", ),
]


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=150,
        unique=True,
    )
    color = ColorField(choices=COLOR_PALETTE)
    slug = models.SlugField(
        'Слаг',
        max_length=150,
        unique=True,
    )

    REQUIRED_FIELDS = ['name', 'color', 'slug']

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=150,
    )
    measurement_unit = models.CharField(
        "Единица измерения",
        max_length=50,
    )

    REQUIRED_FIELDS = ['name', 'measurement_unit']

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipes(models.Model):
    tags = models.ManyToManyField(Tag, through='TagRecipe',
                                  verbose_name='Теги')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngred')
    name = models.CharField(
        'Название',
        max_length=150,
        unique=True,
    )
    image = models.ImageField(
        'Картинка',
        upload_to="recipes/images/",
        default=None
    )
    text = models.CharField(
        'Текстовое описание',
        max_length=150
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    REQUIRED_FIELDS = ['author', 'name', 'image', 'text', 'cooking_time']

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class RecipeIngred(models.Model):
    recipesid = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='recipe_ing',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingred',
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField()

    REQUIRED_FIELDS = ['amount']

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'
        ordering = ['-id']

    def __str__(self):
        return f'{self.recipesid}: {self.ingredient}-{self.amount}'


class TagRecipe(models.Model):
    recipesid = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='recipe_tag',
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag',
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецептов'
        ordering = ['-id']

    def __str__(self):
        return f'{self.recipesid}: {self.tag}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='userfav',
        verbose_name='Пользователь'
    )
    favoriterecipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favrecipe',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списки избранного'
        ordering = ['-id']


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='usershop',
        verbose_name='Пользователь'
    )
    shoprecipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='shoprecipe',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ['-id']
