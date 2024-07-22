from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.account.models import Relation, Profile


@admin.register(Relation)
class RelationModelAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user')


class ProfileInline(admin.StackedInline):
    can_delete = False
    model = Profile


class ExtendedUserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
