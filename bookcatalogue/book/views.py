from django.db.models import Q
from django.views import generic
from .models import Book, Genre, Author, FavoriteBook
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST 
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import redirect


class BookListView(generic.ListView):
    model = Book
    template_name = 'book/index.html' 
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Используем select_related для FK отношений
        queryset = queryset.select_related('genre', 'author')
        
        genre = self.request.GET.get('genre')
        author = self.request.GET.get('author')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if genre:
            queryset = queryset.filter(genre_id=genre)
        if author:
            queryset = queryset.filter(author_id=author)
        if date_from:
            queryset = queryset.filter(publish_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(publish_date__lte=date_to)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['authors'] = Author.objects.all()
        
        if self.request.user.is_authenticated:
            # Получить список книг, находящихся в избранном для текущего пользователя
            favorite_books = set(FavoriteBook.objects.filter(user=self.request.user).values_list('book_id', flat=True))
            context['favorite_books'] = favorite_books
        
        return context

    
class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_favorited'] = FavoriteBook.objects.filter(user=self.request.user, book=self.object).exists()
        return context
    


@login_required
def add_to_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user

    # Проверяем, существует ли запись в избранном для этой книги и пользователя
    favorite, created = FavoriteBook.objects.get_or_create(user=user, book=book)

    if created:
        # Книга добавлена в избранное
        return redirect('book_detail', pk=book_id)
    else:
        # Книга удалена из избранного
        favorite.delete()
        return redirect('book_detail', pk=book_id)

