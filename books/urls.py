# books/urls.py
from django.urls import path
from .views import BookDetailView, BookListView

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("view/<uuid:pk>", BookDetailView.as_view(), name="book_detail"),
]
