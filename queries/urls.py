from django.urls import path,include
from .views import (
 formsetView
)




app_name = "queries"

urlpatterns = [
    path('formset',formsetView,name="formset"),
   
]