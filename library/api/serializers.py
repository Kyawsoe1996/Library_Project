from rest_framework import serializers
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from account.models import Account
from library.models import Book,Author, BorrowBook,Stock,Borrow

#Validator Rest Framework, phone_number validate on Account Serializer
from rest_framework.validators import UniqueValidator


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['id']
        model = Book
        fields = '__all__'
        depth =0
        # extra_kwargs = {'books': {'required': False}}


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = '__all__'
        # depth =1

class BorrowSerializer(serializers.ModelSerializer):
    # book_lists = BookSerializer(many=True)
    class Meta:
        model  = Borrow
        fields = ['user','borrow_date','books']
        # extra_kwargs = {'books': {'required': False,'read_only':True}}


class BorrowBookSerializer(serializers.ModelSerializer):
    # borrows = BorrowSerializer(many=True,read_only=True)
    class Meta:
        model = BorrowBook
        fields = ['id','book_id','qty','user',]
        extra_kwargs = {'borrows': {'required': False}}
        # depth=1





class MyUserSerializer(serializers.ModelSerializer):
    # borrows = BorrowSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = ['id','username']
      



class IssueBookSerializer(serializers.Serializer):
    book_queryset=Book.objects.all()
    user_queryset = User.objects.all()
    user = serializers.IntegerField()
    books = BookSerializer(book_queryset,many=True)
    booking_date = serializers.DateField() 


    def create(self,validated_data):
        import pdb;pdb.set_trace()
        print("Call Create")
        pass


  