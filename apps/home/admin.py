from django.contrib import admin

from apps.home.models import Post


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'slug', 'status')
    prepopulated_fields = {'slug': ('title',)}
