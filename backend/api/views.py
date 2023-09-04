from django.contrib.auth import get_user_model
from django.shortcuts import HttpResponse, render
from djoser.views import UserViewSet
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly, AllowAny)
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication

from recipes.models import Ingredient, Recipe, Tag, User

from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer, OneUserSerializer, ManyUserCreateSerializer, RecipeCreateSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = OneUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    #authentication_classes = (TokenAuthentication,) 

    def get_serializer_class(self):
        if self.action == "create":
            return ManyUserCreateSerializer
        return OneUserSerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,) 

class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,) 
    authentication_classes = (TokenAuthentication,) 

    def get_serializer_class(self):
        if self.action == "create" or self.action == 'partial_update':
            return RecipeCreateSerializer
        return RecipeSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,) 

def index(request):
    return HttpResponse('index')

