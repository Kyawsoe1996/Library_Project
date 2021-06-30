from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import AccountSerializer, RegistrationSerializer,UserSerializer
from account.models import Account
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions

#generic filter
from rest_framework import generics
import django_filters.rest_framework

#searchFilter
from rest_framework import filters
#custom search overide backends
from .backends import CustomSearchFilter

#pagination
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

#viewset
from django.shortcuts import get_object_or_404
from rest_framework import viewsets



#Renderer Usage
from rest_framework.renderers import JSONRenderer




# @api_view(['GET',])
# def account_lists(request):
#     if request.method == "GET":
#         accounts = Account.objects.all()
#         serializer = AccountSerializer(accounts,many=True)
#         return Response(serializer.data)


def validate_email(email):
    account = None
    try:
        account = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    if account != None:
        return email


def validate_username(username):
    account = None
    try:
        account = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    if account != None:
        return username


class AccountView(APIView):
    def get(self, format=None):
        """
        Get all the student records
        :param format: Format of the student records to return to
        :return: Returns a list of student records
        """
        account = Account.objects.all()
        serializer = AccountSerializer(account, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.method == "POST":
            data = {}
            email = request.data.get('user')['email'].lower()
            if validate_email(email) != None:
                data['error_message'] = 'That email is already in use.'
                data['response'] = 'Error'
                return Response(data)
            username = request.data.get('user')['username']
            if validate_username(username) != None:
                data['error_message'] = 'That username is already in use.'
                data['response'] = 'Error'
                return Response(data)
            serializer = AccountSerializer(data=request.data)
            if serializer.is_valid(raise_exception=ValueError):
                account = serializer.create(validated_data=request.data)
                data['response'] = "Successfully register new user"
                data['email'] = account.user.email
                data['username'] = account.user.username
                token = Token.objects.get(user=account.user).key
                data['token'] = token
            else:
                data = serializer.errors
            return Response(data)


@api_view(['POST'])
def registration_view(request):
    import pdb
    pdb.set_trace()
    if request.method == "POST":
        data = {}

        serializer = RegistrationSerializer(request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data,status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # print(serializer)
        return Response(serializer.data)


# Login Token
# class CustomAuthToken(ObtainAuthToken):

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })


class ObtainAuthToken(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = {}
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            
            data['success']= "Successfully Log in"
            data['pk'] = user.pk
            data['username']=user.username
            data['email'] = user.email
            data['token'] = token.key
                    
        
        else:
            data['response'] = "Error"
            data['error_message']="Invalid Credential"
        return Response(data)
   
# Email Validation of Account Update
def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False
        
class AccountPropertiesView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    
    def get(self,request):
        
        data = {}
        user = request.user
        username = user.username
        data['username'] = user.username
        data['email'] = user.email
        return Response(data)
    
    def post(self,request):
        data={}
        user = request.user
        try:
            account= Account.objects.get(user=user)
        except Account.DoesNotExist:
            return Response({"Error":"Not such an username"})
        
        username = request.data['username']
        email = request.data['email']
        email_V = validateEmail(email)
        if email_V is False:
            data["email"] = "Email Format is wrong"
            return Response(data)
            
        
        if account:
            for acc in Account.objects.exclude(id=request.user.accounts.id):
                if acc.user.username == username:
                    data["username"] = "Username already exist"
                    return Response(data)

                if acc.user.email == email.lower():
                    data["email"] = "Email Already exist"
                    return Response(data)
                 
            
            account.user.username = username
            account.user.email = email
            
            account.user.save()
            account.save()
            data["success"]= "Account Updated Successfuly"
            data["user"] = account.user.username
            data["email"] = account.user.email
        else:
            data["error"] = "There is no such account"
            return Response(data)
        return Response(data)
    
class ChangePasswordView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    
    def get(self,request):
        
        data = {}
        try:
            account = Account.objects.get(user=request.user)
        except User.DoesNotExist:
            data["error"] = "User Does Not Exist"
            return Response(data)
        
        old_password = account.user.password
        data['old passsword'] = old_password
        
        
        return Response(data)
    
    def post(self,request):
        data ={}
        user = request.user
        
        try:
            account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            data["error"] = "There is no such account"
            return Response(data)
        posted_data = request.data
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        is_login = authenticate(username=account.user.username,password=old_password)
        print(is_login)
        
        if is_login is None:
            data["old_password"] = "The old password is wrong"
            return Response(data)
        elif not new_password == confirm_password:
            data["error"] = "The two password does not match"
            return Response(data)
        else:
            
            account.user.set_password(confirm_password)
            account.user.save()
            account.save()
            data["success"] ="THe password has been changed successfully"
            
        return Response(data)
    
    
    
##Making Filter with Generic View
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #filter => http://localhost:8000/api/account/generic-filter/?username=zz
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # filterset_fields = ['username']
    
    #search => http://localhost:8000/api/account/generic-filter/?search=admin
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['username','email']
    
    #ordering => http://localhost:8000/api/account/generic-filter/?ordering=username
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email']
    #specifying the default ordering
    ordering = ['username']
    # pagination_class = PageNumberPagination
    #pagination_class = LimitOffsetPagination
    pagination_class = CursorPagination
    
    
#Viewset Django RestFramework Documentation form Django  10-01-2020

# class UserViewSet(viewsets.ViewSet):
#     authentication_classes = [authentication.TokenAuthentication]
#     def list(self,request):
#         queryset = User.objects.all()
#         serializer = UserSerializer(queryset,many=True)
#         return Response(serializer.data)
    
#     def get_permissions(self):
#         if self.action == "list":
            
#             permission_classes = [IsAuthenticated]
#             print(permission_classes,"P##########")
            
#         else:
#             permission_classes = [IsAdmin]
          
#         return [permission() for permission in permission_classes]
 
# Model_View_Set   
# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class = AccountSerializer
#     queryset = Account.objects.all()


    
    
#Renderer Usage from rest_framework documentation API GUide 11-01-2020
class UserCountView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        user_count = User.objects.all().count()
        content = {'user_count': user_count}
        return Response(content)
    
    
    
    
    
    
    
    
    
        
    
        
        
        
        
        
        
    
    
    
        
        
       

        
            
    
    
         
        
