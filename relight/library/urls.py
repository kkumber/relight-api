from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookListView.as_view()),
    path('books/search/', views.BookSearchView.as_view()),
    path('books/bookmark/', views.BookmarkView.as_view()),
    path('books/create/bookmark/page/<slug:slug>', views.BookmarkPageCreateView.as_view()),
    path('books/update/bookmark/page/<slug:slug>', views.BookmarkPageUpdateView.as_view()),
    path('books/details/<slug:slug>/', views.BookDetailView.as_view()),
    path('books/details/<slug:slug>/views/', views.BookViewsUpdateView.as_view()),
    path('books/details/<slug:slug>/likes/', views.BookUpdateLikeView.as_view()),
    path('books/details/<slug:slug>/comments/', views.UserCommentOnBookView.as_view()),
]
    