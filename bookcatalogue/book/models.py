import uuid
from django.db import models
from users.models import BookUser

class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    genre_name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.genre_name


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    publish_date = models.DateField()

    @property
    def average_rating(self):
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
    
    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(BookUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    text = models.TextField()
    
    def __str__(self) -> str:
        return f'Rating for {self.book}'
