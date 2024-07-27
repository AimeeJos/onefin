from django.urls import path, include
from movies import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("collections", views.ListCollection, basename="collections")


urlpatterns = [
    path("", include(router.urls)),
    path("movies", views.ListMovies.as_view()),
]
