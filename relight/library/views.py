from django.shortcuts import render, get_object_or_404
from .models import BookModel, UserCommentOnBookModel
from .serializers import BookSerializer, UserCommentOnBookSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from cloudinary.models import CloudinaryField
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
    
                    
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookModel.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def perform_update(self, serializer):
        serializer.save(likes=[self.request.user])
    
  
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

    