from django.urls import path 
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='home'),
    path('book/<uuid:pk>/', views.BookDetailView.as_view(), name='book_detail'),
]
