from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView 


from .models import Book, Genre, Author 

class BookListView(ListView): 
    model = Book
    template_name = 'book/index.html'
    context_object_name = 'books'
    paginate_by = 10 # Для пагинации на 10 книг на страницу
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = Book.objects.select_related('genre', 'author').all()
        
        # Фильтрация по жанру
        genre = self.request.GET.get('genre')
        if genre:
            queryset = queryset.filter(genre__genre_name=genre)
        
        # Фильтрация по автору
        author = self.request.GET.get('author')
        if author:
            queryset = queryset.filter(author__author_name=author)
        
        # Фильтрация по датам
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from and date_to:
            queryset = queryset.filter(publish_date__range=[date_from, date_to])

        return queryset
