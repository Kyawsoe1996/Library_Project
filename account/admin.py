from django.contrib import admin
from .models import Account
from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ['id','user','phone_number','present_address']


admin.site.register(Account,AccountAdmin)
TokenAdmin.raw_id_fields = ['user']

