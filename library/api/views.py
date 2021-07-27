from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
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
#from .backends import CustomSearchFilter

#pagination
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

#viewset

#for customm issue book
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import serializers
import datetime


from library.models import Book,BorrowBook,Borrow,Stock


from library.models import Book,Author, BorrowBook,Stock,Borrow
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    StockSerializer,
    BorrowSerializer,
    BorrowBookSerializer,
    IssueBookSerializer
)


#Renderer Usage
from rest_framework.renderers import JSONRenderer


class BookViewSet(viewsets.ModelViewSet):
    """
    List all books, or create a new book.
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class StockViewSet(viewsets.ModelViewSet):

    queryset = Stock.objects.all()
    serializer_class = StockSerializer



class BorrowViewSet(viewsets.ModelViewSet):

    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer


class BorrowBookViewSet(viewsets.ModelViewSet):
    queryset = BorrowBook.objects.all()
    serializer_class = BorrowBookSerializer


def overall_method(borrow_book_lists,user,borrow_date):
   """
      Create Borrow Objects Add books to Borrowbook and 
      update status of BB... and book stock  quantity reduce
   """
   today = datetime.datetime.today()
   borrow = Borrow.objects.create(user=user,borrow_date=borrow_date,borrow_status=True)
   print(borrow.books.all(),'#############',borrow.id)
   
   for bor in borrow_book_lists:
      borrow.books.add(bor.id)
   borrow_one_obj = Borrow.objects.get(id=borrow.id)
   for data in borrow_one_obj.books.all():
      #adding_stock_quantity minus after borrowed for the specific book
      stock = Stock.objects.get(book_id=data.book_id)
      stock.avail_qty -= 1
      stock.save()
      data.borrow_status = True
      data.return_date = borrow_one_obj.borrow_date + datetime.timedelta(days=data.book_id.book_expiry_days)
      data.save()

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def IssueBook(request):
    if request.method == "GET":
    # return JsonResponse({"data":"Calling the Issue Book"})
        serializer = IssueBookSerializer()
        return JsonResponse(serializer.data, safe=False)
    else:
        data = JSONParser().parse(request)
        user = data.get('user')
        user = get_object_or_404(User,pk=user)
        account = Account.objects.get(user=user)
        user = account
        #borrow_date got none, so i put as a today date
        borrow_date = data.get('borrow_date')
        borrow_date = datetime.date.today()

        print(borrow_date,'###########')
        books = data.get('books')
       
        
        for book in books:
            #its int, get of book object
            book = get_object_or_404(Book,id=book)

            if book.stocks.all()[0].avail_qty <= 0:
                name = book.name
                data = "Not enough stock of %s book" %name
                raise serializers.ValidationError({'error':data})
        
        books = Book.objects.filter(id__in=books)
        
        book_lists = [book.id for book in books]
        print(book_lists,"BOOk_LISTS")
        borrow_book_lists = []

        for b in book_lists:
            book = get_object_or_404(Book,id=b)
            user = get_object_or_404(Account,id=user.id)
            print(user,"####################################s")
            if Borrow.objects.filter(user=user,books__book_id__id__in=book_lists,borrow_status=True).exists():
               pass
            else:
               borrow_book,created = BorrowBook.objects.get_or_create(
                                    book_id=book,user=user,borrow_status=False,return_status=False
                                    )
               borrow_book_lists.append(borrow_book)


        user = get_object_or_404(Account,id=user.id) 
        borrow_qs_all = Borrow.objects.filter(user=user,borrow_status=True)
        if borrow_qs_all.exists():
            #checking the duplicate borrow books
            for borrow_qs in borrow_qs_all:
                for i in BorrowBook.objects.filter(user=user,borrow_status=True):
                    for book in books:
                        for data in book.b_books.all():
                            if data in borrow_qs.books.all():
                                # messages.info(request," Book -  %s  already booked" %data.book_id.name)
                                name = "Already Booked for this  %s" % data.book_id.name
                                return JsonResponse({"data":name})

            #if there is no duplicate book,  then create another borrow_obj
            overall_method(borrow_book_lists,user,borrow_date)
        
        else:
            overall_method(borrow_book_lists,user,borrow_date=borrow_date)

           

        

        return JsonResponse({"success":"Successfully Booked"})
    











        # serializer = IssueBookSerializer(data=data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return JsonResponse(serializer.data, status=201)
        # return JsonResponse(serializer.errors, status=400)
    #return JsonResponse({"data":"Not a POST REQUEST"})


