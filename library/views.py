from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .form import BookForm
from .models import Book
# Create your views here.


def home_view(request):
   return render(request,"library/admin_view.html")

def BookRegister(request,id=0):
   if request.method == 'GET':
      if id == 0:
         form = BookForm()
      else:
         book = Book.objects.get(pk=id)
         form = BookForm(instance=book)


      return render(request,"library/book_register.html",{"form":form})
   else:
      if id == 0:
         form=BookForm(request.POST, request.FILES)
      else:
         book = Book.objects.get(pk=id)
         form = BookForm(request.POST,request.FILES, instance=book)
      if form.is_valid():
         form.save()
      return redirect("library:book-list")


def BookList(request):
   books = Book.objects.all()
   context =  {
      "books":books
   }
   return render(request,'library/book_list.html',context)


def BookDelete(request,id):
   book = Book.objects.get(pk=id)
   book.delete()
   return redirect("library:book-list")