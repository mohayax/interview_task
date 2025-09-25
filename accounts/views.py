from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema



class SignUp(APIView):
    permission_classes = [AllowAny,]
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: UserSerializer},
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)