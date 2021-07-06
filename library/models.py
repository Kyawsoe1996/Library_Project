from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import Account
import datetime
# Create your models here.

CATEGORY = (
    ('En', 'Entertainment'),
    ('Te', 'Technology'),
    ('Sc', 'Science'),
    ('En','Engineering'),
    ('Ps','Psycology'),
)
class Author(models.Model):
    

    author_name = models.CharField(max_length=200)
    author_dob = models.DateField()
    

    class Meta:
       

        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
       return self.author_name

class Config(models.Model):
    name = models.CharField(max_length=150)
    books_fine = models.IntegerField()
    books_expiry_days = models.IntegerField()
    books_lost = models.IntegerField()
    

    class Meta:
        

        verbose_name = 'Config'
        verbose_name_plural = 'Configs'

    def __str__(self):
        
        return self.name


class Book(models.Model):
    """Model definition for MODELNAME."""
    name = models.CharField(max_length=300,unique=True)
    category = models.CharField(choices=CATEGORY, max_length=2)
    published_date= models.DateField()
    isbn = models.CharField(max_length=50)
    author = models.ForeignKey(Author,
                             on_delete=models.CASCADE)
    image = models.ImageField()
    book_expiry_days = models.IntegerField()
    book_fine = models.IntegerField()
    
    



    

    class Meta:
        """Meta definition for MODELNAME."""

        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.name

#Stock
class Stock(models.Model):
    """Model definition for Stock."""

    book_id = models.ForeignKey(Book,related_name="stocks",on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        """Meta definition for Stock."""

        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'

    def __str__(self):
        return '%d of %s' % (self.quantity, self.book_id.name)



# When Create Book Automatically create Stock
@receiver(post_save, sender=Book)
def create_stock_when_create_book(sender, instance=None, created=False, **kwargs):
    if created:
        Stock.objects.create(book_id=instance)





class BorrowBook(models.Model):
    

    book_id = models.ForeignKey('Book',related_name="b_books",on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    borrow_status = models.BooleanField(default=False)
    return_date = models.DateField(blank=True,null=True)

    class Meta:
       

        verbose_name = 'BorrowBook'
        verbose_name_plural = 'BorrowBooks'

    def __str__(self):
       
        return '%d of %s by  %s' % (self.qty, self.book_id.name,self.user)


class Borrow(models.Model):
    

    user = models.ForeignKey(Account, related_name='accounts', on_delete=models.CASCADE)
    books = models.ManyToManyField(BorrowBook)
    borrow_date = models.DateField()
    return_date = models.DateField(blank=True,null=True)
    borrow_status = models.BooleanField(default=False)
    return_status = models.BooleanField(default=False)


    
    class Meta:
        

        verbose_name = 'Borrow'
        verbose_name_plural = 'Borrows'

    def __str__(self):
       
        return '%s' % self.user
    
    # def calculate_expiray_date(self):
    #     for i in self.books.all():
    #         config = Config.objects.all()[0]
    #         if config:
    #             adding_date = self.borrow_date + datetime.timedelta(days=config.books_expiry_days)
    #         else:
    #             adding_date = self.borrow_date + datetime.timedelta(days=10)
    #         return_date = adding_date
    #         return return_date
    
    def calculate_fine(self):
        
        
        # print(self.return_date)
        today = datetime.date.today()
        for data in self.books.all():
            if data.return_date < today:
                #getting timedelta
                days = today - data.return_date
                #get the day difference in integer
                days = days.days
                return days * data.book_id.book_fine
            else:
                return ''


        
        # if self.return_date < today:
        #     #getting timedelta
        #     days = today - self.return_date
        #     #get the days difference in integer
        #     days = days.days
        #     config = Config.objects.all()[0]
        #     if config:

        #         return days * config.books_fine
        #     else:
        #         return days * 1000
        # else:
        #     return ''




        
        
        
        

        





        

        
