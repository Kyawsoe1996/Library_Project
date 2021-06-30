from django.db import models

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
        
