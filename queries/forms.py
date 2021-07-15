from django import forms
from django.forms import formset_factory
from django.forms import BaseFormSet

#Work with formset
from django.forms import inlineformset_factory
from .models import Order,Item,Customer


class BaseArticleFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields["my_field"] = forms.CharField()

class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()


#Working with formset
OrderForSet =inlineformset_factory(Customer,Order,fields=('item','qty','description'))







   