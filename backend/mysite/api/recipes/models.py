from django.db import models


class Tag(models.Model):
    name = models.CharField(
        "Название",
        max_length=150,
        unique=True,
    )
    color = models.CharField(
        "Цветовой HEX-код",
        max_length=14,
        unique=True,
    )
    slug = models.SlugField(
        "Слаг",
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
        "Название",
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
    ingredients = models.ManyToManyField(Ingredient, through='RecipIngred')
    name = models.CharField(
        "Название",
        max_length=150,
        unique=True,
    )

    REQUIRED_FIELDS = ['name']

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
        related_name='recipesid'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient'
    )
    amount = models.IntegerField()

    class Meta:
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'
        ordering = ['-id']

    def __str__(self):
        return f'{self.recipesid} {self.ingredient} {self.amount}'
