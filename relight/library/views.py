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
    queryset = BookModel.objects.all().order_by('title')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = BookListPagination

    def perform_create(self, serializer):
        # Save the instance with the user
        book_instance = serializer.save(uploaded_by=self.request.user)

        # Extract file name from the PDF URL
        if book_instance.pdf_file:
            pdf_url = book_instance.pdf_file.url
            pdf_file_name = os.path.basename(pdf_url).split(".")[0]

            # Set the title to the PDF file name if no title was provided
            book_instance.title = book_instance.title or pdf_file_name
            book_instance.save()



                    
class BookDetailView(generics.RetrieveAPIView):
    queryset = BookModel.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
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