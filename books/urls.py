# books/urls.py
from django.urls import path
from .views import BookDetailView, BookListView, get_recommended_books, like_book

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("view/<uuid:pk>", BookDetailView.as_view(), name="book_detail"),
    path("like/<uuid:id>", like_book, name="like_book"),
    path("recommended/", get_recommended_books, name="recommended_books"),
]
