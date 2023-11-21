from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )
    empty_value_display = 'Поле не заполнено'
    list_editable = ('role',)
    list_filter = ('username',)
    list_per_page = 10
    search_fields = ('username', 'role')
