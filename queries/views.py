from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .forms import ArticleForm
from django.forms import formset_factory
from .forms import BaseArticleFormSet
import datetime
# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.forms import inlineformset_factory
from .models import Customer,Order,Item


def formsetView (request):
    # ArticleFormSet = formset_factory(ArticleForm,extra=3,)
    # formset = ArticleFormSet
    # context = {
    #     'form':formset(initial=[
    #         {'title':'Django is now open source',
    #         'pub_date':datetime.date.today()
    #         }
    #     ])
    # }
    # return render(request,'queries/index.html',context)
    ArticleFormSet = formset_factory(ArticleForm,extra=3,can_delete=True)
    if request.method == 'POST':
        formset = ArticleFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            pass
    else:
        formset = ArticleFormSet(
            initial=[{
                'title':"Django",
                'pub_date':datetime.date.today()
            }]
        )

    

    return render(request, 'queries/index.html', {'formset': formset})



#Working with Formset

def add_orders(request,**kwargs):
    
    customer_id = kwargs.get('customer_id')
    #print(customer_id)
    try:

        customer = Customer.objects.get(pk=customer_id)
    
    except ObjectDoesNotExist:
        return HttpResponse("No customer found in db")
    
    OrderInlineFormSet =inlineformset_factory(Customer,Order,
                            fields=('item','qty','description'))
    
    if request.method == 'POST':
        formset = OrderInlineFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return HttpResponse("Successfully Added")

    
    formset = OrderInlineFormSet(instance=customer)
    context = {
        'formset':formset
    }

   
    
    return render(request,"queries/formset/index.html",context)