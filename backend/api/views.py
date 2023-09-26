from http import HTTPStatus

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import Cart, Favourite, Ingredient, Recipe, Tag
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import Follow, User

from .filters import RecipeFilter
from .pagination import LimitNumberPagination
from .serializers import (CartSerializer, FavouriteSerializer,
                          FollowCreateSerializer, IngredientSerializer,
                          ManyUserCreateSerializer, OneUserSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          TagSerializer)
from .utils import cart_down


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = OneUserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitNumberPagination

    def get_serializer_class(self):
        if self.action == "create":
            return ManyUserCreateSerializer
        return OneUserSerializer

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowCreateSerializer(
            pages, many=True, context={
                'request': request})
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        user = request.user
        author = User.objects.get(id=id)
        if request.method == 'POST':
            if author != user and not Follow.objects.filter(
                    user=user, author=author).exists():
                serializer = FollowCreateSerializer(Follow.objects.create(
                    author=author, user=user), context={'request': request})
                return Response(serializer.data)
        else:
            if Follow.objects.filter(author=author, user=user).exists():
                unfollow = Follow.objects.filter(author=author, user=user)
                unfollow.delete()
                return Response(status=HTTPStatus.NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = LimitNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == "create" or self.action == 'partial_update':
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            serializer = FavouriteSerializer(
                Favourite.objects.create(
                    recipe=recipe, user=user))
            return Response(serializer.data)
        else:
            if Favourite.objects.filter(recipe=recipe, user=user).exists():
                unfollow = Favourite.objects.filter(recipe=recipe, user=user)
                unfollow.delete()
                return Response(status=HTTPStatus.NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        return cart_down(request)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            serializer = CartSerializer(
                Cart.objects.create(
                    recipe=recipe, user=user))
            return Response(serializer.data)
        else:
            if Cart.objects.filter(recipe=recipe, user=user).exists():
                unfollow = Cart.objects.filter(recipe=recipe, user=user)
                unfollow.delete()
                return Response(status=HTTPStatus.NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class IngredientViewSet(ModelViewSet):
    pagination_class = None
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
