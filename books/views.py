# books/views.py
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from books.tasks import create_book_recommendations
from .models import Book, BookRecommendation, BookUserLikes


User = get_user_model()


@login_required
def index(request):
    return render(request, "books/index.html")


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

    extra_context = {"has_liked_book": False}

    def get_object(self):
        obj = super().get_object()
        user_id = self.request.user.id
        has_liked_book = obj.has_user_liked_book(user_id)
        self.extra_context["has_liked_book"] = has_liked_book
        if has_liked_book:
            self.extra_context["recommendations"] = BookRecommendation.objects.filter(
                source__pk=obj.id, user__pk=user_id
            )[:4]
        return obj


class RecommendedBooksView(LoginRequiredMixin, ListView):
    model = BookRecommendation
    context_object_name = "book_list"
    login_url = "account_login"
    paginate_by = 12
    template_name = "books/recommended.html"

    def get_queryset(self):
        return super().get_queryset().filter(user__pk=self.request.user.id)


class LikedBooksView(LoginRequiredMixin, ListView):
    model = BookUserLikes
    context_object_name = "book_list"
    login_url = "account_login"
    paginate_by = 12
    template_name = "books/book_list_liked.html"

    def get_queryset(self):
        return super().get_queryset().filter(user__pk=self.request.user.id)


@login_required
def like_book(request, id):
    book = Book.objects.get(pk=id)

    if book is None:
        messages.error(request, "Book not found!")
        return redirect(BookListView)

    user = User.objects.get(pk=request.user.id)

    liked_book = BookUserLikes(user=user, book=book)
    liked_book.save()

    create_book_recommendations.delay(request.user.id, book.id)

    return redirect(reverse("book_detail", args=[id]))
