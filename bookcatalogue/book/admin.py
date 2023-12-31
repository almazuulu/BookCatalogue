from django.contrib import admin
from .models import Author, Book, Genre, Review, FavoriteBook

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name']
    search_fields = ['first_name', 'last_name']

    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre_name']
    search_fields = ['genre_name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'author', 'publish_date']
    list_filter = ['genre', 'author']
    search_fields = ['title', 'genre']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating']
    search_fields = ['name']


admin.site.register(FavoriteBook)