from django.urls import  path,include

from rest_framework.authtoken import views
#router for viewset
from rest_framework.routers import DefaultRouter
from .views import BookViewSet,AuthorViewSet,StockViewSet

router = DefaultRouter()

app_name = "library"
#router.register(r'api/users', UserViewSet, basename='user')
#router.register(r'api/authors', AuthorViewSet, basename='author')

urlpatterns = [
    
]
router.register(r'books', BookViewSet, basename='book')
router.register(r'authors', AuthorViewSet, basename='author'),
router.register(r'stocks', StockViewSet, basename='stock'),




urlpatterns += router.urls