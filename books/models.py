import uuid
from django.db import models
from django.urls import reverse

from common.models.recommended import RecommenderModel


# Create your models here.
class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField()
    author = models.CharField(max_length=200)
    image_link = models.TextField()
    genre = models.CharField(max_length=200)
    rating = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])


class BookRecommendation(RecommenderModel):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="recommendation",
    )
