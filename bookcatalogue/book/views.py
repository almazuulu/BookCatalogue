from django.db.models import Q
from django.views import generic
from .models import Book, Genre, Author

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
        return context
    

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book/book_detail.html'