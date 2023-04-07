# books/views.py
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    paginate_by = 12
    context_object_name = "book_list"
    template_name = "books/book_list.html"
    login_url = "account_login"


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    context_object_name = "book"
    login_url = "account_login"
    template_name = "books/book_detail.html"
