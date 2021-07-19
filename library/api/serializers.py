from rest_framework import serializers
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from account.models import Account
from library.models import Book,Author,Stock,Borrow

#Validator Rest Framework, phone_number validate on Account Serializer
from rest_framework.validators import UniqueValidator


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['id']
        model = Book
        fields = '__all__'
        # extra_kwargs = {'books': {'required': False}}


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = '__all__'

class BorrowSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Borrow
        fields = '__all__'

  