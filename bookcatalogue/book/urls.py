from django.urls import path 
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='home'),
    path('book/<uuid:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<uuid:book_id>/add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('book/<uuid:book_id>/remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),
]


