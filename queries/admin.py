from django.contrib import admin

# Register your models here.

from .models import Blog
from .models import Author
from .models import Entry
from .models import Article


from .models import Order,Item,Customer


admin.site.register(Blog)
admin.site.register(Author)
admin.site.register(Entry)
admin.site.register(Article)


admin.site.register(Customer)
admin.site.register(Item)
admin.site.register(Order)
