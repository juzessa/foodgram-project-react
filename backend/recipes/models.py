from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .constants import COLOR, TWOHUNDRED


class Tag(models.Model):
    name = models.CharField(max_length=TWOHUNDRED)
    color = models.CharField(max_length=COLOR)
    slug = models.SlugField(max_length=TWOHUNDRED, unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name or ''


class Ingredient(models.Model):
    name = models.CharField(max_length=TWOHUNDRED)
    measurement_unit = models.CharField(max_length=TWOHUNDRED)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_measure'
            ), )

    def __str__(self):
        return self.name or ''


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes')
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient')
    image = models.ImageField(upload_to='images/', blank=True)
    text = models.TextField()
    name = models.CharField(max_length=TWOHUNDRED)
    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1, message='Так быстро ничего не приготовится'),
            MaxValueValidator(60)])
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name or ''


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, null=True, on_delete=models.SET_NULL)
    ingredient = models.ForeignKey(
        Ingredient, null=True, on_delete=models.SET_NULL)
    amount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1, message='Нужно добавить что-то'),
            MaxValueValidator(60)])

    class Meta:
        verbose_name = 'РецептИнгредиент'
        verbose_name_plural = 'РецептИнгредиенты'

    def __str__(self):
        return self.recipe or ''


class RecipeTag(models.Model):
    recipe = recipe = models.ForeignKey(
        Recipe, null=True, on_delete=models.SET_NULL)
    tag = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'РецептТэг'
        verbose_name_plural = 'РецептТэги'


class BaseContent(models.Model):
    recipe = models.ForeignKey(Recipe, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Favourite(BaseContent):

    class Meta:
        verbose_name = 'Любимое'
        verbose_name_plural = 'Любимые'


class Cart(BaseContent):

    class Meta:
        verbose_name = 'Корзина'
