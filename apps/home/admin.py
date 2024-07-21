from django.contrib import admin

from apps.home.models import Post, Vote


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'slug', 'status')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body',)
    list_filter = ('status',)
    raw_id_fields = ('user',)


@admin.register(Vote)
class VoteModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'post',)
