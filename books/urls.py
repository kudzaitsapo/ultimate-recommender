# books/urls.py
from django.urls import include, path
from .views import BookDetailView, BookListView, LikedBooksView, RecommendedBooksView, index, like_book

urlpatterns = [
    path("", index, name="book_index_page"),
    path("all-books/", BookListView.as_view(), name="book_list"),
    path("liked-books/", LikedBooksView.as_view(), name="liked_books"),
    path("view/<uuid:pk>", BookDetailView.as_view(), name="book_detail"),
    path("like/<uuid:id>", like_book, name="like_book"),
    path("recommended/", RecommendedBooksView.as_view(), name="recommended_books"),
    path("search/", include("haystack.urls")),
]
