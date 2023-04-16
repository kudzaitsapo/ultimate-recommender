# books/urls.py
from django.urls import include, path
from .views import BookDetailView, BookListView, get_recommended_books, index, like_book

urlpatterns = [
    path("", index, name="index_page"),
    path("all-books/", BookListView.as_view(), name="book_list"),
    path("view/<uuid:pk>", BookDetailView.as_view(), name="book_detail"),
    path("like/<uuid:id>", like_book, name="like_book"),
    path("recommended/", get_recommended_books, name="recommended_books"),
    path("search/", include("haystack.urls")),
]
