from .forms import RegisterCustomUser, ChangeCustomUser
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib import admin


class CustomUserAdmin(UserAdmin):
    add_form = RegisterCustomUser
    form = ChangeCustomUser
    model = CustomUser

    list_display = [
        'username',
        "email",
        "age",
        "gender",
    ]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'age', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'age', 'gender'),
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
