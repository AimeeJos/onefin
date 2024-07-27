from movies.models import Movies, Collections
from rest_framework import views, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from movies.serializers import MovieSerializer, CollectionSerializer
from django.core.paginator import Paginator

import requests

def get_request_for_movies():
    url = "https://freetestapi.com/api/v1/movies"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
    

    
class ListCollection(viewsets.ModelViewSet):
    queryset = Collections.objects.all()
    serializer_class = CollectionSerializer    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            "user": self.request.user
            })
        return context
    
class ListMovies(views.APIView):
    def get(self, request):        
        data = get_request_for_movies()        
        return Response(data)
    
    
    
    
