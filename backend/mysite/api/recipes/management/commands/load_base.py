import csv

from api.recipes.models import Ingredient
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open(
            f'{settings.BASE_DIR}/ingredients.csv',
            'r',
            encoding='utf-8'
        ) as csv_file:
            id = 1
            reader = csv.DictReader(csv_file)
            Ingredient.objects.bulk_create(
                Ingredient(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Загрузка завершена!'))
