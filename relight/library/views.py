from django.shortcuts import render, get_object_or_404
from .models import BookModel, UserCommentOnBookModel, BookmarkModel
from .serializers import BookSerializer, UserCommentOnBookSerializer, BookmarkSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from cloudinary.models import CloudinaryField
from rest_framework.views import APIView
from rest_framework.response import Response
import io
import requests
import fitz
from cloudinary.utils import cloudinary_url
import cloudinary
import os

# Create your views here.
class BookListPagination(PageNumberPagination):
    page_size = 20

class BookListView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = BookListPagination

    def perform_create(self, serializer):
        # Save the instance with the user
        book_instance = serializer.save(uploaded_by=self.request.user)
        book_instance.save()
    
    def get_queryset(self):
        sort = self.request.query_params.get('sort_by', 'title')
        return BookModel.objects.all().order_by(sort)
        
class BookSearchView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = BookListPagination

    def get_queryset(self):
        query = self.request.query_params.get('search_query', None);
        if query:
            return BookModel.objects.filter(title__istartswith=query)
        return BookModel.objects.none()
    
class BookmarkView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = BookModel.objects.filter(likes=self.request.user)
        return queryset
    
                    
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookModel.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class BookUpdateLikeView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, slug):
        book = BookModel.objects.get(slug=slug)
        if request.user in book.likes.all():
            book.likes.remove(request.user)
            return Response({'message': 'Removed from Library'})
        else:
            book.likes.add(request.user)
            return Response({'message': 'Added to Library'})


class BookViewsUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, slug):
        book = BookModel.objects.get(slug=slug)
        book.views += 1
        book.save()
        return Response({'message': 'Viewed'}, status=200)
    
  
class UserCommentOnBookView(generics.ListCreateAPIView):
    serializer_class = UserCommentOnBookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        book = get_object_or_404(BookModel, slug=slug)
        return UserCommentOnBookModel.objects.filter(specific_book=book)
    
    def perform_create(self, serializer):
        slug = self.kwargs['slug']
        book = get_object_or_404(BookModel, slug=slug)
        serializer.save(owner=self.request.user, specific_book=book)


class BookmarkPageCreateView(generics.ListCreateAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        slug = self.kwargs['slug']
        book = get_object_or_404(BookModel, slug=slug)
        serializer.save(book=book, user=self.request.user)
        
    def get_queryset(self):
        slug = self.kwargs['slug']
        book = get_object_or_404(BookModel, slug=slug)
        return BookmarkModel.objects.filter(specific_book=book, user=self.request.user)
    

class BookmarkPageDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        slug = self.kwargs['slug']
        book = get_object_or_404(BookModel, slug=slug)
        return BookmarkModel.objects.filter(user=user, book=book)

    
    