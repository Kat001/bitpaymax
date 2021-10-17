from django.contrib import admin
from .models import Account
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'sponsor', 'is_active1', 'date_active')
    search_fields = ('email', 'username',)
    readonly_fields = ('username',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.unregister(Group)
admin.site.register(Account,AccountAdmin)