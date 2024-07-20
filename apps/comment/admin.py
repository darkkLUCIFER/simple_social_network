from django.contrib import admin

from apps.comment.models import Comment


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'is_reply',)
    list_filter = ('is_reply',)
