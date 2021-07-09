from django.urls import path,include
from .views import (
    home_view,
    BookRegister,
    BookList,
    BookDelete,
    BorrowBooks,
    ViewIssueBook,
    ReturnBook,
)




app_name = "library"

urlpatterns = [
    path('',home_view,name="home"),
    #books
    path('book_register/',BookRegister,name="book-register"),
    path('book-list',BookList,name="book-list"),
    path('<int:id>/', BookRegister,name='book-update'), # get and post req. for update operation
    path('delete/<int:id>/',BookDelete,name='book-delete'),
    path('borrow-book/',BorrowBooks,name="borrow-books"),

    #Issue Book
    path('view-issue-book/',ViewIssueBook.as_view(),name="view-issue-book"),

    #Return Book
    path('return-book/<int:id>/',ReturnBook,name="return-book")
]