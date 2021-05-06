from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from spend.models import User, Familie, Transaction, Categorie

admin.site.unregister(Group)

class UsersAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_superuser')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, UsersAdmin)
admin.site.register(Familie)
admin.site.register(Categorie)
admin.site.register(Transaction)