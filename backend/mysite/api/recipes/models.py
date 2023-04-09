from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=150,
        unique=True,
    )
    color = models.CharField(
        'Цветовой HEX-код',
        max_length=14,
        unique=True,
    )
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
        max_length=5,
    )

    REQUIRED_FIELDS = ['name', 'measurement_unit']

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Recipes(models.Model):
    tags = models.ManyToManyField(Tag, through='TagRecip')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(Ingredient, through='RecipIngred')
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
    cooking_time = models.IntegerField(
        'Время приготовления в минутах'
    )

    REQUIRED_FIELDS = ['name', 'image', 'text', 'cooking_time']

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-id']

    def __str__(self):
        return self.name


class RecipIngred(models.Model):
    recipesid = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='recip_ing'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingred'
    )
    amount = models.IntegerField()

    REQUIRED_FIELDS = ['amount']

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'
        ordering = ['-id']

    def __str__(self):
        return f'{self.recipesid}: {self.ingredient}-{self.amount}'


class TagRecip(models.Model):
    recipesid = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='recip_tag'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag'
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецептов'
        ordering = ['-id']

    def __str__(self):
        return f'{self.recipesid}: {self.tag}'
