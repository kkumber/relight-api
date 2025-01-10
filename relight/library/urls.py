from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookListView.as_view()),
    path('books/details/<slug:slug>/', views.BookDetailView.as_view()),
    path('books/details/<slug:slug>/comments/', views.UserCommentOnBookView.as_view()),
]
 