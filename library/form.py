from django.forms import ModelForm
from django import forms
from .models import Book,Borrow
from django.utils.safestring import mark_safe
import datetime

class CustomChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        # return mark_safe("<img src='%s' width='100px'/>"   % obj.image.url)
        return "{}".format(obj.name)
        #  return "{} | {}".format(obj.val_a, obj.val_b
        
        # return mark_safe('<a href="%s">%s</a> <img src="%s" width="100px" />' % (obj.name, obj.image.url))
        


       

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
        



class BorrowForm(forms.ModelForm):
    

    class Meta:
        """Meta definition for Borrowform."""

        model = Borrow
        exclude = ["return_date","borrow_status","return_status"]
        widgets = {
        'borrow_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'placeholder':'Select a date', 'type':'date'}),
            }

    def __init__(self, *args, **kwargs):
        super(BorrowForm,self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = "Select Student"

        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})
        
        self.fields["books"].widget = forms.widgets.CheckboxSelectMultiple()
        # self.fields["books"].help_text = ""
        self.fields["books"].queryset = Book.objects.all()
        #self.fields["books"] = CustomChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Book.objects.all())
        
        self.fields["books"].help_text=""
        self.fields["books"].empty_label = None

    # def clean(self):
    #     print("#Is valid method called")
    #     user = self.clean_data["user"]
    #     print("####User")
    #     return self.clean_data 


