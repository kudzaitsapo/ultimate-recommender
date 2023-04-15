from __future__ import absolute_import, unicode_literals

from books.helper import is_book_already_recommended_to_user
from .models import BookRecommendation, Book
from recommendations.books.recommender import recommend_book
from django.contrib.auth import get_user_model
from celery.utils.log import get_task_logger


from celery import shared_task

logger = get_task_logger(__name__)


User = get_user_model()


@shared_task
def add(x, y):
    return x + y


"""
Algorithm to recommend books based on a user's liked books:
1. For each liked book
    1.1. Get recommendations
    1.2. Check if the recommendations are not already part of the existing recommendations
    1.3. Add to the database
"""


@shared_task()
def create_book_recommendations(user_id, liked_book_id):
    user = User.objects.get(pk=user_id)
    book = Book.objects.get(pk=liked_book_id)
    new_recommendations = recommend_book(book.title)
    logger.info("Length of recommendations dataframe: {}".format(str(len(new_recommendations.index))))
    for item in new_recommendations.itertuples():
        if not is_book_already_recommended_to_user(item.id, user):
            recommended_book = Book.objects.get(pk=item.id)
            recommendation = BookRecommendation(book=recommended_book, user=user, source=book)
            recommendation.save()
            logger.info("Recommended book {} to {}".format(item.title, user))
        else:
            logger.info("Book {} has already been recommended to {}".format(item.title, user))
