from rest_framework import views, viewsets, generics, status
from rest_framework.response import Response
from core.serializers import UserSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()

class RequestCount(views.APIView):
    def get(self, request):
        count = cache.get('request_count', 0)
        return Response({"requests": count})


class ResetCount(views.APIView):
    def get(self, request):
        cache.set('request_count', 0)
        count = cache.get('request_count', 0)
        return Response({"requests": count})
    
    
class CreateUser(generics.CreateAPIView):
    """Create a new user in the system"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListUsers(generics.ListAPIView):
    """List all users in the system"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLogin(views.APIView):
    """user login"""

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "success": True,
                "status": status.HTTP_200_OK,
                "data": serializer.data,
                "message": "Login successful",
            },
            status=status.HTTP_200_OK,
        )
