from .models import BookRecommendation


def is_book_already_recommended_to_user(book_id, user):
    recommendation = BookRecommendation.objects.filter(user=user, book__pk=book_id)
    return recommendation.first() is not None
