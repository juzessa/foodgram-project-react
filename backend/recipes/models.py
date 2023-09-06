
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField(max_length=200, unique=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes')
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient')
    image = models.ImageField(upload_to='images/', blank=True)  # поправить
    text = models.TextField()
    name = models.CharField(max_length=200)
    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1, message='Так быстро ничего не приготовится')])
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, null=True, on_delete=models.SET_NULL)
    ingredient = models.ForeignKey(
        Ingredient, null=True, on_delete=models.SET_NULL)
    amount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1, message='Нужно добавить что-то')])


class RecipeTag(models.Model):
    recipe = recipe = models.ForeignKey(
        Recipe, null=True, on_delete=models.SET_NULL)
    tag = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL)

# class Favourite(models.Model): #хз
    # pass

# class Cart(models.Model):
   # pass
