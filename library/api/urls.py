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
    ViewIssueBook,
    )


router = DefaultRouter()

app_name = "library"
#router.register(r'api/users', UserViewSet, basename='user')
#router.register(r'api/authors', AuthorViewSet, basename='author')

urlpatterns = [
    path('issue-book',IssueBook,name="ib"),
    # path('v-i-b/',ViewIssueBook.as_view()),name="v_i_b")
    path('v-i-b/',ViewIssueBook.as_view({'get':'list'}),name="ib"),


    
]
router.register(r'books', BookViewSet, basename='book')
router.register(r'authors', AuthorViewSet, basename='author'),
router.register(r'stocks', StockViewSet, basename='stock'),
router.register(r'borrow',BorrowViewSet,basename="borrow"),
router.register(r'borrow-book',BorrowBookViewSet,basename="borrow-books")
# router.register(r'v-i-b',ViewIssueBook,basename="v_i_b")






urlpatterns += router.urls