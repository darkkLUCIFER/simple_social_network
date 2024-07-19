from django.contrib.auth.models import User
from django.db import models

from apps.utils.base_model import BaseModel


class Relation(BaseModel):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name='Follower')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings', verbose_name='Following')

    def __str__(self):
        return f'{self.from_user} following {self.to_user}'

    class Meta:
        db_table = 'relation'
        verbose_name = 'Relation'
        verbose_name_plural = 'Relations'
