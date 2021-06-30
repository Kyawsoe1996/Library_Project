from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=200)
    email = forms.EmailField()
    phone_number = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    present_address = forms.CharField(max_length=300)



    def clean_email(self):
        email = self.cleaned_data.get('email').lower()

        try:
            account = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % email)

    def clean_username(self):
        account = self.cleaned_data.get('username').lower()

        try:
            account = User.objects.get(username=account)
        except User.DoesNotExist:
            return account
        raise forms.ValidationError('Account "%s" is already in use.' % account)
    

    def clean(self):
       cleaned_data = super().clean()
       
       password = cleaned_data.get('password')
       confirm_password = cleaned_data.get('confirm_password')
       msg = "Passwords are not match"
       if password != confirm_password:
           self.add_error('password',msg)
           self.add_error('confirm_password',msg)




class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('email', 'username', )

	def clean_email(self):
        
		email = self.cleaned_data['email'].lower()
		try:
			account = User.objects.exclude(pk=self.instance.pk).get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % email)

	def clean_username(self):
        
		username = self.cleaned_data['username']
		try:
			account = User.objects.exclude(pk=self.instance.pk).get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)


class ChangePassword(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','password','new_password','confirm_password')

        labels = {
           
            "password":"Old password",
            'new_password':'New Password',
            'confirm_password':'Confirm Password'
        }
    

    # def clean_password(self):
    #     import pdb;pdb.set_trace()
    #     old_password = self.cleaned_data.get('password')
    #     try:
    #        user=User.objects.get(password=old_password)
    #     except User.DoesNotExist:
    #        return old_password
    #     raise forms.ValidationError("No old password")

    # def clean(self):
       
    #    cleaned_data = super().clean()
       
    #    new_password = cleaned_data.get('new_password')
    #    confirm_password = cleaned_data.get('confirm_password')
    #    msg = "Passwords are not match"
    #    if new_password != confirm_password:
    #        self.add_error('new_password',msg)
    #        self.add_error('confirm_password',msg)
    #    else:
    #        return cleaned_data
       


       







        
        
        








