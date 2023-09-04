from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import (Ingredient, Recipe, RecipeIngredient, RecipeTag,
                            Tag, User)


class OneUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class ManyUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')

class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

class RecipeTagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True, source='recipeingredient_set')

    class Meta:
        model = Recipe
        fields = '__all__'
    
    #def create(self, validated_data):
        #tags = validated_data.pop('tags')
        #ingredients = validated_data.pop('ingredients')
        #author = self.context.get('request').user
       # recipe = Recipe.objects.create(author=author, **validated_data)
        #for tag in tags:
          #  RecipeTag.objects.create(tag=tag, recipe=recipe) ## не сработает
        #for ingr in ingredients:
           # ingredient = Ingredient.objects.get(id=ingr['id'])
           # RecipeIngredient.objects.create(
              #  ingredient=ingredient, recipe=recipe, amount=ingr['amount']
          #  )
        #return recipe
    
    #def update(self, instance, validated_data):
        #tags = validated_data.pop('tags')
        #удалять старые теги и ингредиенты
        #pass

class RecipeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name', 'text', 'cooking_time')

class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'