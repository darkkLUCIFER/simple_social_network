from django.contrib import admin

from apps.account.models import Relation, Profile


@admin.register(Relation)
class RelationModelAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user')


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'bio')
