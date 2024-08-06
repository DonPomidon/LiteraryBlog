from django.contrib import admin
from .models import Author, Category, Book, Review


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
    list_display = ['book', 'user', 'comment', 'rating']
    list_filter = ['user', 'rating']


@admin.register(Author)
class ModelNameAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
