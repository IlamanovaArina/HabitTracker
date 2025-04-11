from django.contrib import admin

from users.models import User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone']
    list_filter = ['name', 'id']
