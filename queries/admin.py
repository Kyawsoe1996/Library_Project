from django.contrib import admin

# Register your models here.

from .models import Blog
from .models import Author
from .models import Entry
from .models import Article


admin.site.register(Blog)
admin.site.register(Author)
admin.site.register(Entry)
admin.site.register(Article)

