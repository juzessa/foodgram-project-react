import csv

from django.core.management.base import BaseCommand

from foodgram_backend import settings
from recipes.models import Ingredient

PATH = f'{settings.BASE_DIR}/data/'


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        file_name = 'ingredients.csv'
        with open(PATH + file_name, mode="r", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name, measurement_unit = row
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=measurement_unit)
        self.stdout.write(self.style.SUCCESS('Загружено.'))
