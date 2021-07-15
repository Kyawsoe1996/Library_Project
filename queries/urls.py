from django.urls import path,include
from .views import (
 formsetView,
 add_orders,
)




app_name = "queries"

urlpatterns = [
    path('formset',formsetView,name="formset"),
    path('add_order/<str:customer_id>/',add_orders, name='add-orders')
   
]