from django.urls import  path,include
from .views import (
    registration_view,
    # account_lists,
    AccountView,
    # CustomAuthToken,
    ObtainAuthToken,
    AccountPropertiesView,
    ChangePasswordView,
    UserListView,
    
    #Viewset
    # UserViewSet,
   
    #renderer usage
    UserCountView,
)

from rest_framework.authtoken import views
#router for viewset
from rest_framework.routers import DefaultRouter





app_name = "account"
urlpatterns = [
    path('register/',registration_view,name="register-view"),
    path('users/',AccountView.as_view(),name="user-list"),
    #default token adding => In postman provide username, pass by POSt, it will get token
    path('api-token-auth/', views.obtain_auth_token),
    # path('api-token-auth/',CustomAuthToken.as_view(),name="auth-token"),
    #cutomize login token
    path('login/',ObtainAuthToken.as_view(),name="login"),
    #get Account Info Via Api call, and Update account name and email via Json data with POST call, Json=>{"username":"Kaw","email":"kyaw@gmail.com"}
    path('properties/',AccountPropertiesView.as_view(),name="account-properties"),
    path('change-password/',ChangePasswordView.as_view(),name="change-password"),
    path("generic-filter/",UserListView.as_view(),name="generic-filter"),
    #renderer usage
    path("renderer/",UserCountView.as_view(),name="renderer")
    
    #ViewSet
    # path("viewsets/",UserViewSet.as_view({'get': 'list'}),name="viewset")
]


#ViewSet with Router
# router = DefaultRouter()
# router.register('userd',UserViewSet,basename="user")
# urlpatterns += router.urls


#ViewSet with Router
# router = DefaultRouter()
# router.register("articles",ArticleViewSet,basename="article")
# urlpatterns += router.urls


