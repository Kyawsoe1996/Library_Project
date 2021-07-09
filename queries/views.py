from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .forms import ArticleForm
from django.forms import formset_factory
from .forms import BaseArticleFormSet
import datetime
# Create your views here.


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
