from django.contrib import admin
from .models import Book,Author,Stock,Borrow,BorrowBook,Config
# Register your models here.

# admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Stock)


class BorrowAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
       
        'get_books',
        'borrow_date',
        'return_date',
        'borrow_status',
        'return_status'
    ]

    search_fields = ['user__user__username']
    def get_books(self, obj):
        return "\n".join([str(p) for p in obj.books.all()])

admin.site.register(Borrow, BorrowAdmin)

class BooksAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        # 'pulished_date',
        
        
        'isbn',
        'author',
        'category',


    ]

    search_fields = [
        'author__author_name'
    ]

admin.site.register(Book, BooksAdmin)


class BorrowBookAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'book_id',
        'qty',
        'user',
        'borrow_status',
    ]
    list_filter = [
        'book_id',
        'user',
        'borrow_status'
    ]
    list_display_links =[
        'book_id',
        'user'
    ]
    search_fields =[
        'user__user__username'
    ]

admin.site.register(BorrowBook, BorrowBookAdmin)


class ConfigAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'books_fine',
        'books_expiry_days',
        'books_lost',
    ]

admin.site.register(Config, ConfigAdmin)









