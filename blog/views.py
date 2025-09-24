from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    def get(self, request):
        blogs = Blog.objects.all().order_by('-created_at')
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(blogs, request)
        serializer = BlogSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    
    @swagger_auto_schema(
    request_body=BlogSerializer,
    responses={201: BlogSerializer},
    )
    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
    request_body=BlogSerializer,
    responses={200: BlogSerializer},
    )
    def put(self, request, id):
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        serializer = BlogSerializer(blog, data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            blog.updated_at = datetime.now()
            blog.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        blog.delete()
        return Response({'message': 'Blog deleted'}, status=status.HTTP_204_NO_CONTENT)  


class BlogLikeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id):
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if user in blog.likes.all():
            blog.likes.remove(user)
            blog.updated_at = datetime.now()
            blog.save()
            return Response({'message': 'Blog unliked'}, status=status.HTTP_200_OK)  
        else:
            blog.likes.add(user)
            blog.updated_at = datetime.now()
            blog.save()
            return Response({'message': 'Blog liked'}, status=status.HTTP_200_OK)

    



class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=CommentSerializer,
        responses={201: CommentSerializer},
    )
    def post(self, request, id):
        data = request.data
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'body': request.data.get('body'),
            'blog': blog.id
        }
        serializer = CommentSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save(author=request.user)
            blog.updated_at = datetime.now()
            blog.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
    request_body=CommentSerializer,
    responses={200: CommentSerializer}
    )
    def put(self, request, id):
        try:
            comment = Comment.objects.get(id=id).select_related('blog')
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'body': request.data.get('body'),
            'blog': comment.blog.id
        }

        serializer = CommentSerializer(comment, data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            blog = comment.blog
            blog.updated_at = datetime.now()
            blog.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            comment = Comment.objects.get(id=id).select_related('blog')
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        blog = comment.blog
        comment.delete()
        blog.updated_at = datetime.now()
        blog.save()
        return Response({'message': 'Comment deleted'}, status=status.HTTP_204_NO_CONTENT)