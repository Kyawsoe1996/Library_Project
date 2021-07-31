from django.shortcuts import render,redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .form import BookForm,BorrowForm
from .models import Book,BorrowBook,Borrow,Stock
import datetime
from account.models import Account
from django.contrib.auth.decorators import login_required

# Create your views here.


def home_view(request):

   return redirect("library:book-list")

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





#code become duplicate, thats why making resuable
#1. Creating borrow object,
#2. Inside the borrow obj, adding borrow book list
#3. After borrow, adding the stock quantity of the books  minus---1
#4. Adding return date on borrow book obj
#5 Adding borrow_status true in borrow_book obj
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



# Borrow Book
def BorrowBooks(request):
   if request.method == "GET":
      form = BorrowForm()
      context = {
         "form":form,
      }
      return render(request,'library/borrow-book.html',context)
   else:
      form =BorrowForm(request.POST or None)
      if form.is_valid():
         user = form.cleaned_data.get("user")
         books = form.cleaned_data.get("books")
         borrow_date = form.cleaned_data.get("borrow_date")
         print(datetime.datetime.today())


         # checking first for the availabe book qty
         for book in books:
            if book.stocks.all()[0].avail_qty <= 0:
               messages.info(request,"You don't have enough %s book in stock...Pls add to stock" % book.name )
               return redirect("library:borrow-books") 
         
            
         
         book_lists = [book.id for book in books]
         borrow_book_lists = []
         for b in book_lists:
            book = get_object_or_404(Book,id=b)
            if Borrow.objects.filter(user=user,books__book_id__id__in=book_lists,borrow_status=True).exists():
               pass
            else:
               borrow_book,created = BorrowBook.objects.get_or_create(
                                    book_id=book,user=user,borrow_status=False,return_status=False
                                    )
               borrow_book_lists.append(borrow_book)
         # print(book_lists)
         # print(borrow_book_lists)

         borrow_qs_all = Borrow.objects.filter(user=user,borrow_status=True)
         if borrow_qs_all.exists():
            #checking the duplicate borrow books
            for borrow_qs in borrow_qs_all:
            
               for i in BorrowBook.objects.filter(user=user,borrow_status=True):
                  for book in books:

                     for data in book.b_books.all():
                        if data in borrow_qs.books.all():
                           messages.info(request," Book -  %s  already booked" %data.book_id.name)
                           return redirect("library:book-list")

            #if there is no duplicate book,  then create another borrow_obj
            overall_method(borrow_book_lists,user,borrow_date)

         else:
            #newly created borrow objects.
            overall_method(borrow_book_lists,user,borrow_date)

         
         return redirect("library:book-list")



class ViewIssueBook(View):
   def get(self, request, *args, **kwargs):
      #authentication check for non-login users
      if self.request.user.username == '':
         messages.info(self.request, "You need to login")
         return redirect("account:login")
      user = self.request.user
      if user.is_superuser:
         borrow_qs_all = Borrow.objects.filter(borrow_status=True).order_by('borrow_date')
         # context ={
         # "borrow_qs_all":borrow_qs_all
         # } 
      else:

         account = Account.objects.get(user=user)
         borrow_qs_all = Borrow.objects.filter(user=account,borrow_status=True).order_by('borrow_date')
       #by_date
      context ={
         "borrow_qs_all":borrow_qs_all
      }

      return render(self.request,'library/view_issue_book.html',context)
        

   def post(self, request, *args, **kwargs):
      return HttpResponse('POST request!')



def ReturnBook(request,id):
   print(id,'########')
   borrow_book_obj = BorrowBook.objects.get(id=id)
   borrow_book_obj.return_status = True
   borrow_book_obj.borrow_status  = False
   borrow_book_obj.save()
   
   print(borrow_book_obj)
   #for stock increment after book return
   stock = Stock.objects.get(book_id=borrow_book_obj.book_id)
   
   stock.avail_qty += 1
   stock.save()

   
   borrow_obj =  Borrow.objects.get(id=borrow_book_obj.borrow_set.all()[0].id)
   tup_list  =[]
   for borrow_book_obj in borrow_obj.books.all():
      status = borrow_book_obj.return_status
      tup_list.append(status)
     
  #print(tuple(tup_list), "TUP TUP TUP TUP")
   return_status_lists = []
   return_status_lists.append(tuple(tup_list))
 
   all_return_inside_borrow_obj = [ all(val == True for val in tup) for tup in return_status_lists]
   if all_return_inside_borrow_obj[0]  == True:
      print("All books in the borrow object are returned")
      borrow_obj.return_status = True
      borrow_obj.borrow_status = False
      borrow_obj.save()
   else:
      print("Still Remaining")


   
   return redirect("library:view-issue-book")
         
