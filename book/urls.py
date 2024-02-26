from django.urls import path
from . import views
 
urlpatterns = [
    path('details/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('borrowed/<int:pk>', views.BookReviewView.as_view(), name='borrowed_book'),
    path('user-borrowed-books/<int:pk>', views.BorrowBook, name="borrow_book"),
    path("return-book/<int:pk>", views.ReturnBook, name="return_book")
]