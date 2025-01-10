from django.shortcuts import render, get_object_or_404
from .models import BookModel, UserCommentOnBookModel
from .serializers import BookSerializer, UserCommentOnBookSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
import fitz
from cloudinary.models import CloudinaryField

# Create your views here.
class BookListPagination(PageNumberPagination):
    page_size = 20


class BookListView(generics.ListCreateAPIView):
    queryset = BookModel.objects.all().order_by('title')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = BookListPagination
    
    
    def perform_create(self, serializer):
        book_instance = serializer.save(uploaded_by=self.request.user)
        
        if book_instance.pdf_file:
            pdf_path = book_instance.pdf_file.path
            with fitz.open(pdf_path) as doc:
                book_instance.author = book_instance.author or doc.metadata.get('author', 'Unknown')
                book_instance.title = book_instance.title or doc.metadata.get('title', 'Untitled')
                
                if not book_instance.book_cover:
                    page = doc[0]
                    pix = page.get_pixmap()
                    cover_path = f"cover_{book_instance.id}.png"
                    pix.save(cover_path)
                    book_instance.book_cover = CloudinaryField(cover_path)
                    
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