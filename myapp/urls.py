from django.urls import path
from . import views

urlpatterns = [

    path('user/register/', views.register_user, name='register_user'),
    path('user/login/', views.user_login, name='user_login'),
    

    path('books/', views.list_books, name='list_books'),
    path('books/create/', views.create_book, name='create_book'),
    path('books/<int:book_id>/', views.get_book_details, name='book_details'),
    

    path('book-request/create/', views.create_book_request, name='create_book_request'),
    path('book-request/list/', views.list_book_requests, name='list_book_requests'),
    path('book-request/history/', views.book_request_history, name='book_request_history'),
    path('book-request/<int:request_id>/approve/', views.approve_book_request, name='approve_book_request'),
    path('book-request/<int:request_id>/deny/', views.deny_book_request, name='deny_book_request'),
]