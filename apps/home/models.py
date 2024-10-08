from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from apps.utils.base_model import BaseModel


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100, verbose_name='Title')
    body = models.TextField(verbose_name='Body')
    slug = models.SlugField(verbose_name='Slug')
    status = models.BooleanField(default=True, verbose_name='Status')

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def get_absolute_url(self):
        return reverse('home:post_detail', kwargs={'post_slug': self.slug, 'post_id': self.pk})

    def likes_count(self):
        return self.votes.count()

    def user_can_like(self, user):
        """
            Check if user can like this post or not
        """
        user_like = user.votes.filter(post=self)
        if user_like.exists():
            return False
        return True

    class Meta:
        db_table = 'post'
        ordering = ('-created_at',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Vote(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes', verbose_name='Vote')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes', verbose_name='Post')

    def __str__(self):
        return f'{self.user} voted on {self.post.slug}'

    class Meta:
        db_table = 'vote'
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
