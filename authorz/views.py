from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema

from time import sleep
from . import serializers
from .tasks import upload_file
from .renderers import UserJSONRenderer
from .serializers import RegistrationSerializer, LoginSerializer, PostSerializer, FileUploadSerializer
from .models import Post, User
from .permissions import IsOwnerOrReadOnly

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.save()
            sleep(7)
            upload_file.delay(file.id) 
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)
    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
