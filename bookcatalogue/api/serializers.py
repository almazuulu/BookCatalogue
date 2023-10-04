from rest_framework import serializers
from book.models import Author, Genre, Book, Review, FavoriteBook
from users.models import BookUser


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        depth = 1  # чтобы показать связанные поля ForeignKey


class ReviewSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=BookUser.objects.all())
    rating = serializers.IntegerField()
    text = serializers.CharField()

    class Meta:
        model = Review
        fields = ('id', 'book', 'user', 'rating', 'text')



class FavoriteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteBook
        fields = '__all__'