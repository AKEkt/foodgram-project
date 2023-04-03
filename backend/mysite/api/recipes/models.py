from django.db import models


class Tag(models.Model):
    name = models.CharField(
        "Название",
        max_length=150,
    )
    color = models.CharField(
        "HEX-код",
        max_length=14,
    )
    slug = models.SlugField(
        "Слаг",
        unique=True,
    )

    REQUIRED_FIELDS = ['name', 'color', 'slug']

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']

    def __str__(self):
        return self.name
