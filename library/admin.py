from django.contrib import admin
from .models import Book,Author,Stock,Borrow,BorrowBook
# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Stock)
admin.site.register(Borrow)
admin.site.register(BorrowBook)