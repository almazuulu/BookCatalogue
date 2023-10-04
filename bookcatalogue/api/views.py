from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from book.models import Book, FavoriteBook, Review
from .serializers import BookSerializer, ReviewSerializer

class BookViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Book.objects.select_related('genre', 'author').all()
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
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

    @action(detail=True, methods=['POST'])
    def add_review(self, request, *args, **kwargs):
        book = self.get_object()
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(book=book, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def toggle_favorite(self, request, *args, **kwargs):
        book = self.get_object()
        favorite, created = FavoriteBook.objects.get_or_create(user=request.user, book=book)
        
        if created:
            return Response({"status": "added to favorites"}, status=status.HTTP_201_CREATED)
        else:
            favorite.delete()
            return Response({"status": "removed from favorites"}, status=status.HTTP_200_OK)
