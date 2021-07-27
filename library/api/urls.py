from django.urls import  path,include

from rest_framework.authtoken import views
#router for viewset
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet,
    AuthorViewSet,
    StockViewSet,
    BorrowViewSet,
    BorrowBookViewSet,
    IssueBook,
    )


router = DefaultRouter()

app_name = "library"
#router.register(r'api/users', UserViewSet, basename='user')
#router.register(r'api/authors', AuthorViewSet, basename='author')

urlpatterns = [
    path('issue-book',IssueBook,name="ib")
    
]
router.register(r'books', BookViewSet, basename='book')
router.register(r'authors', AuthorViewSet, basename='author'),
router.register(r'stocks', StockViewSet, basename='stock'),
router.register(r'borrow',BorrowViewSet,basename="borrow"),
router.register(r'borrow-book',BorrowBookViewSet,basename="borrow-books")




urlpatterns += router.urls