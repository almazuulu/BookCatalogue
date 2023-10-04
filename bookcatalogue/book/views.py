from django.db.models import Q
from django.views import generic
from .models import Book, Genre, Author, FavoriteBook
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


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
            
        # Если пользователь авторизован, добавляем информацию о избранном
        if self.request.user.is_authenticated:
            favorite_books = set(FavoriteBook.objects.filter(user=self.request.user).values_list('book_id', flat=True))
            for book in queryset:
                book.is_favorite = book.id in favorite_books

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['authors'] = Author.objects.all()
        return context
    

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    
    


@login_required
@require_POST
def add_to_favorites(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    favorite, created = FavoriteBook.objects.get_or_create(user=request.user, book=book)

    if created:
        return JsonResponse({'status': 'added', 'message': 'Книга добавлена в избранное'})
    else:
        return JsonResponse({'status': 'already_added', 'message': 'Книга уже в избранном'})


@login_required
@require_POST
def remove_from_favorites(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    favorite = FavoriteBook.objects.filter(user=request.user, book=book).first()

    if favorite:
        favorite.delete()
        return JsonResponse({'status': 'removed', 'message': 'Книга удалена из избранного'})
    else:
        return JsonResponse({'status': 'not_found', 'message': 'Книга не найдена в избранном'})
