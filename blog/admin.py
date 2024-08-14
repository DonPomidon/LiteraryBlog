from django.contrib import admin
from .models import Author, Category, Book, Review, CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import CreateCustomUser, ChangeCustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CreateCustomUser
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


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'description', 'category', 'rating', 'added_by', 'publish']
    list_filter = ['author', 'category', 'rating', 'added_by', 'publish']
    search_fields = ['title', 'description']
    raw_id_fields = ['author']
    ordering = ['publish']
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'comment', 'rating', 'created']
    list_filter = ['user', 'rating']
    search_fields = ['user', 'book', 'comment']


@admin.register(Author)
class ModelNameAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(CustomUser, CustomUserAdmin)
