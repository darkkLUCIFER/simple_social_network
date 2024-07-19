from django.contrib import admin

from apps.account.models import Relation


@admin.register(Relation)
class RelationModelAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user')
