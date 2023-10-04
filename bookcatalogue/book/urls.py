from django.urls import path 
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='home'),
    path('book/<uuid:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('add_to_favorite/<uuid:book_id>/', views.add_to_favorite, name='add_to_favorite'),
    path('book/<uuid:pk>/add_review/', views.BookDetailView.as_view(), name='add_review'),
]





