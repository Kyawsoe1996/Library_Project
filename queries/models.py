from django.db import models

# Create your models here.
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField()
    number_of_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.headline


#Working with model form set

class Article(models.Model):
    
    title = models.CharField(max_length = 100)
    pub_date = models.DateField()
    # TODO: Define fields here

    class Meta:
        

        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        
        return self.title



#Checking with the INline formset factory

class Customer(models.Model):
    
    name = models.CharField(max_length=25)
    def __str__(self):
        return self.name


class Item(models.Model):
    
    name = models.CharField(max_length = 25)

    def __str__(self):
        return self.name

class Order(models.Model):
    
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    description = models.TextField()


    def __str__(self):
        return self.customer.name

    # def __unicode__(self):
    #     return 


    
