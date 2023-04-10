# books/views.py
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.serializers import serialize
from django.contrib.auth.mixins import LoginRequiredMixin

from books.tasks import create_book_recommendations
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

    def post(self, request, *args, **kwargs):
        bookId = self.get_object().pk

        create_book_recommendations.delay(request.user.id, liked_book_ids=[bookId])

        resp = dict(message="Successfully done something")
        return JsonResponse(resp, content_type="application/json")
