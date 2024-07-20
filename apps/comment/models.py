from django.contrib.auth.models import User
from django.db import models

from apps.home.models import Post
from apps.utils.base_model import BaseModel


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='User')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Post')
    reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies',
                              verbose_name='Reply')
    is_reply = models.BooleanField(default=False, verbose_name='Is reply?')
    body = models.TextField(max_length=400, verbose_name='Comment')

    def __str__(self):
        return f'{self.user} {self.post}'

    class Meta:
        db_table = 'comment'
        ordering = ('-created_at',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
