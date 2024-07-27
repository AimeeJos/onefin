from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()


class Movies(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=250, null=True, blank=True)
    genres = models.CharField(max_length=100, null=True, blank=True)
    uuid = models.UUIDField(null=True, blank=True)


class Collections(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=250, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_collections", null=True, blank=True
    )
    movies = models.ManyToManyField(
        Movies, related_name="movies_collection", null=True, blank=True
    )

    @property
    def favourite_genres(self):
        genres = (
            self.movies.values("genres")
            .annotate(count=Count("genres"))
            .order_by("-count")[:3].values_list("genres", flat=True)
        )
        return genres
