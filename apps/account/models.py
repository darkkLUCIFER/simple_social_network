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


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveSmallIntegerField(default=0, verbose_name='Age')
    bio = models.TextField(null=True, blank=True, verbose_name='Bio')

    def __str__(self):
        return f'{self.user}'

    class Meta:
        db_table = 'profile'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
