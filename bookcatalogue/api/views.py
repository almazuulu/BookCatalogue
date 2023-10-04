from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from book.models import Book, FavoriteBook
from .serializers import BookSerializer, ReviewSerializer

class BookViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Book.objects.select_related('genre', 'author').all()
    serializer_class = BookSerializer

    def get_queryset(self):
        return self._filter_queryset(super().get_queryset())

    def _filter_queryset(self, queryset):
        filters = {
            'genre_id': self.request.GET.get('genre'),
            'author_id': self.request.GET.get('author'),
            'publish_date__gte': self.request.GET.get('date_from'),
            'publish_date__lte': self.request.GET.get('date_to')
        }

        for key, value in filters.items():
            if value:
                queryset = queryset.filter(**{key: value})

        return queryset

    @action(detail=True, methods=['POST'])
    @authentication_classes([JSONWebTokenAuthentication])
    @permission_classes([IsAuthenticated])
    def add_review(self, request, *args, **kwargs):
        book = self.get_object()
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(book=book, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    @authentication_classes([JSONWebTokenAuthentication])
    @permission_classes([IsAuthenticatedOrReadOnly])
    def toggle_favorite_status(self, request, *args, **kwargs):
        book = self.get_object()
        favorite, created = FavoriteBook.objects.get_or_create(user=request.user, book=book)

        if created:
            return Response({"status": "added to favorites"}, status=status.HTTP_201_CREATED)

        favorite.delete()
        return Response({"status": "removed from favorites"}, status=status.HTTP_200_OK)
