"""Serializers"""

from rest_framework import serializers
from movies.models import Movies, Collections
from core.serializers import UserSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class MovieSerializer(serializers.ModelSerializer):
    """Movie Serializer"""

    class Meta:
        model = Movies
        fields = ["title", "description", "genres", "uuid"]


class CollectionSerializer(serializers.ModelSerializer):
    """Collection Serializer"""

    # user = UserSerializer()
    movies = MovieSerializer(many=True)
    favourite_genres = serializers.ReadOnlyField()

    class Meta:
        model = Collections
        fields = ['id',"title", "description", "movies", "favourite_genres"]

    def create(self, validated_data):
        user = self.context.get("user", None)
        movies = validated_data.pop("movies", [])
        user = User.objects.get(id=user.id) 
        coll_obj = Collections.objects.create(**validated_data)
        coll_obj.user = user
        print(movies, type(movies))
        coll_movies = []
        if movies:
            for movie in movies:
                movie_obj = Movies.objects.create(**movie)
                coll_movies.append(movie_obj)
            
        coll_obj.movies.set(coll_movies)
        coll_obj.save()
        return coll_obj
    
    def update(self, instance, validated_data):
        movies = validated_data.pop("movies", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        coll_movies = []
        if movies:
            for movie in movies:
                movie_obj = Movies.objects.create(**movie)
                coll_movies.append(movie_obj)
            
        instance.movies.set(coll_movies)
        instance.save()
        return instance
