from django.forms import ModelForm
from django import forms
from .models import Book

class BookForm(ModelForm):
    """Form definition for Book."""

    class Meta:
        """Meta definition for Bookform."""

        model = Book
        fields = ['name','category','published_date','isbn','author','image']
        widgets = {
        'published_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'placeholder':'Select a date', 'type':'date'}),
    }
        # labels = {
        #     'category':'Select Categories',
            
        # }


    def __init__(self, *args, **kwargs):
        super(BookForm,self).__init__(*args, **kwargs)
        self.fields['author'].empty_label = "Select Author"
        
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})


        #adding the form widght as form-control in model form    
        # self.fields['name'].widget.attrs.update({'class': 'form-control'})
        


