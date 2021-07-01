from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import Account
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


class Book(models.Model):
    """Model definition for MODELNAME."""
    name = models.CharField(max_length=300)
    category = models.CharField(choices=CATEGORY, max_length=2)
    published_date= models.DateField()
    isbn = models.CharField(max_length=50)
    author = models.ForeignKey(Author,
                             on_delete=models.CASCADE)
    image = models.ImageField()
    



    

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


class Borrow(models.Model):
    

    user = models.ForeignKey(Account, related_name='accounts', on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    borrow_date = models.DateTimeField(auto_now=True)
    return_date = models.DateTimeField(blank=True,null=True)
    borrow_status = models.BooleanField(default=False)
    return_status = models.BooleanField(default=False)


    
    class Meta:
        

        verbose_name = 'Borrow'
        verbose_name_plural = 'Borrows'

    def __str__(self):
       
        return '%s' % (self.user)


class BorrowBook(models.Model):
    

    book_id = models.ForeignKey('Book',related_name="b_books",on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    borrow_status = models.BooleanField(default=False)

    class Meta:
       

        verbose_name = 'BorrowBook'
        verbose_name_plural = 'BorrowBooks'

    def __str__(self):
       
        return '%d of %s' % (self.qty, self.book_id.name)





        

        
