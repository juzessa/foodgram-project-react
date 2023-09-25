from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email',
        'first_name', 'last_name', )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'first_name')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('author', 'user',)
    list_filter = ('author',)
