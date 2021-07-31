from django.db.models.query import QuerySet
from rest_framework import serializers
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
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
    
# class UsernameshowingField(serializers.RelatedField):
    
#     def to_representation(self, value):
#         import pdb;pdb.set_trace()
#         print("value")
#         return value

class ViewIssueBookSerializer(serializers.ModelSerializer):
    # filters = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    books = serializers.SerializerMethodField()
    class Meta:
        model = Borrow
        exclude = ['return_date','borrow_status','return_status','id']
        ordering =['user']

    # def to_representation(self, instance):
    #     import pdb;pdb.set_trace()
    #     # print("Calling to reprensetnatin...............")
    #     # ret = super().to_representation(instance)
    #     # ret['user'] = ret['user']
    #     # acc = Account.objects.get(user__id=ret['user'])
    #     # ret['user'] = acc.user.username
    #     # return instance
    #     acc = Account.objects.get(user=instance.user.user) 
    #     return {
    #         "user":acc.user.username
    #     }

    def get_books(self,obj):
        books = []
        for book in obj.books.all():
            print("book",book.book_id.name)
            books.append(book.book_id.name)
        return books


    def get_user(self,obj):
        acc= Account.objects.get(user=obj.user.user)
        return acc.user.username

    # def get_filters(self, obj):
    #     # import pdb;pdb.set_trace()
    #     print(obj,'###############')
    #     data = {
    #         "books":[],
    #         "data":"RUXK"
    #     }
    #     return data

# class ViewIssbo(serializers.Serializers):
#       user = serializers.IntegerField()
#       date = serializers.DateField()

  