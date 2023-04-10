import uuid
from django.db import models
from django.contrib.auth import get_user_model


class RecommenderModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
