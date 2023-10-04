from django.db.models import Q
from django.views import generic
from .models import Book, Genre, Author, FavoriteBook, Review
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .forms import ReviewForm


class BookListView(generic.ListView):
    model = Book
    template_name = 'book/index.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('genre', 'author')
        filters = self._get_filters_from_request()
        return queryset.filter(**filters)

    def _get_filters_from_request(self):
        filters = {}

        genre = self.request.GET.get('genre')
        if genre:
            filters['genre_id'] = genre

        author = self.request.GET.get('author')
        if author:
            filters['author_id'] = author

        date_from = self.request.GET.get('date_from')
        if date_from:
            filters['publish_date__gte'] = date_from

        date_to = self.request.GET.get('date_to')
        if date_to:
            filters['publish_date__lte'] = date_to

        return filters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['authors'] = Author.objects.all()

        if self.request.user.is_authenticated:
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

        context['reviews'] = Review.objects.filter(book=self.object)
        context['review_form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = self._save_review(review_form, book, request.user)
            return redirect('book_detail', pk=book.pk)
        else:
            context = self.get_context_data()
            context['review_form'] = review_form
            return self.render_to_response(context)

    def _save_review(self, review_form, book, user):
        review = review_form.save(commit=False)
        review.book = book
        review.user = user
        review.save()
        return review


@login_required
def add_to_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user
    favorite, created = FavoriteBook.objects.get_or_create(user=user, book=book)

    if not created:
        favorite.delete()

    return redirect('book_detail', pk=book_id)
