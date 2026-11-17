from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import Post, Comment
from .serializers import (
    PostSerializer,
    PostDetailSerializer,
    PostValidateSerializer,
    CommentSerializer,
    CommentValidateSerializer,
)



@swagger_auto_schema(method='post', request_body=PostValidateSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list_api_view(request):
    if request.method == 'GET':
        posts = Post.objects.filter(is_published=True).order_by('-created_at')
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = PostValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = Post.objects.create(
            author=request.user,
            title=serializer.validated_data.get('title'),
            body=serializer.validated_data.get('body'),
            is_published=serializer.validated_data.get('is_published'),
        )
        return Response(data=PostDetailSerializer(post).data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='put', request_body=PostValidateSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail_api_view(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(data={'error': 'Post not found!'}, status=status.HTTP_404_NOT_FOUND)

   
    if not post.is_published and post.author != request.user:
        return Response(data={'error': 'Post not found!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = PostDetailSerializer(post).data
        return Response(data=data)

    
    if post.author != request.user:
        return Response(data={'error': 'Вы не автор этого поста!'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = PostValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        post.title = serializer.validated_data.get('title')
        post.body = serializer.validated_data.get('body')
        post.is_published = serializer.validated_data.get('is_published')
        post.save()
        return Response(data=PostDetailSerializer(post).data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='post', request_body=CommentValidateSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_comments_api_view(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(data={'error': 'Post not found!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        comments = Comment.objects.filter(post=post, is_approved=True).order_by('-created_at')
        data = CommentSerializer(comments, many=True).data
        return Response(data=data)

    elif request.method == 'POST':
        serializer = CommentValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            body=serializer.validated_data.get('body'),
            is_approved=serializer.validated_data.get('is_approved'),
        )
        return Response(data=CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='put', request_body=CommentValidateSerializer)
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_detail_api_view(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return Response(data={'error': 'Comment not found!'}, status=status.HTTP_404_NOT_FOUND)

    if comment.author != request.user:
        return Response(data={'error': 'Вы не автор этого комментария!'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = CommentValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment.body = serializer.validated_data.get('body')
        comment.is_approved = serializer.validated_data.get('is_approved')
        comment.save()
        return Response(data=CommentSerializer(comment).data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
