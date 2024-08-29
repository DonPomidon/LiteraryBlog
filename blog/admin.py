from django.contrib import admin
from .models import Author, Category, Book, Review


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'description', 'category', 'added_by', 'publish']
    list_filter = ['author', 'category', 'added_by', 'publish']
    search_fields = ['title', 'description']
    ordering = ['publish']
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'comment', 'created']
    list_filter = ['user']
    search_fields = ['user', 'book', 'comment']


@admin.register(Author)
class ModelNameAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
