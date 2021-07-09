from django import forms
from django.forms import formset_factory
from django.forms import BaseFormSet


class BaseArticleFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields["my_field"] = forms.CharField()

class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()






   