from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .forms import RegistrationForm,AccountUpdateForm,ChangePassword
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Account
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import View
import pyotp
from datetime import datetime
import base64



# Create your views here.

@login_required
def home(request):
    return render(request,"account/index.html")

def logout_fn(request):
    logout(request)
    return redirect("account:register")

def check_username_and_email(username,email):
    username = username.lower()
    email = email.lower()


    


def account_detail(request):
    if request.method == "GET":
        user = User.objects.get(username=request.user)
        context = {
            'user':user
        }
        
        return render(request,'account/account_detail.html',context)
    else:
        context = {}
        form = AccountUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            context['success_message'] = "Updated"
            return render(request,'account/account_detail.html',context)
        else:
            form = AccountUpdateForm(request.POST)
            context ={
                'form':form
            }
            
            
            return render(request,'account/account_detail.html',context)

       
        
        
def login_fn(request):
    if request.method == "GET":
        return render(request,'account/login.html')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user:
               
                # login(request, user)
                # messages.info(request,'Successfully login as '+ str(user.username))
                return redirect("account:otp",phone=user.accounts.phone_number)

            else:
                
                context = {
                    "data":"Invalid Login",
                    
                }
               
                return render(request,"account/login.html",context)

        # return JsonResponse(request.POST)


def register(request):
    if request.method == "GET":
        form = RegistrationForm()
        context = {
            'form':form
        }
        return render(request,'account/register.html',context)
    else:
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            phone_number = form.cleaned_data.get('phone_number')
            present_address = form.cleaned_data.get('present_address')
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            account = Account.objects.get(user=user)
            account.phone_number=phone_number
            account.present_address = present_address
            account.save()
            messages.info(request,"Successfully created")
            
            return redirect("account:login")
        else:
            form = RegistrationForm(request.POST)
            context = {
                'form':form
            }
            
            return render(request,'account/register.html',context)
        return redirect("account:login")

def change_password(request):
    context={}
    if request.POST:
        print(request.POST)
        password = request.POST['password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = User.objects.get(username=request.user)
        user_authenticate = authenticate(request, username=request.user, password=password)
        form= ChangePassword()
        if not new_password == confirm_password:
            context.update({"not_match":"Passwords Not matched","form":form})
        
        elif user_authenticate is None:
            context.update({"old_password":"Old password is wrong","form":form})
        
        else:
            user.set_password(confirm_password)
            user.save()
            messages.info(request,"Password Updated Successfully")
            return redirect("account:login")
        


            
    else:
        form = ChangePassword()
        context['form'] = form

        
    return render(request,'account/change_password.html',context)


#OTP_COde
def returnValue(phone):
    return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


class CounterBaseOTPView(View):
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(self.request,"You have already logged in")
            return redirect("account:home")
        
        phone = kwargs.get("phone")
        print(phone)
        try:
            acc = Account.objects.get(phone_number=phone)
        except ObjectDoesNotExist:
            messages.info(self.request,"Your number is not registered")
            return redirect("account:register")
        acc.counter +=1
        acc.save()
        key =  base64.b32encode(returnValue(phone).encode())
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        #print(OTP.at(acc.counter))
        #print(key)
        otp_code = OTP.at(acc.counter)
        context ={
            "otp":otp_code
        }
        
        
        return render(self.request,"account/otp_view.html",context)

    def post(self, request, *args, **kwargs):
        import pdb;pdb.set_trace()
        phone = kwargs.get('phone')
        try:
            acc = Account.objects.get(phone_number=phone)
        except ObjectDoesNotExist:
            messages.info("Phone Does Not Exist")
            return redirect("account:login",)  # False Call
        key =  base64.b32encode(returnValue(phone).encode())
        OTP = pyotp.HOTP(key)  # HOTP Model
        if OTP.verify(request.POST["otp"], acc.counter):  # Verifying the OTP
            acc.isVerified = True
            acc.save()
            login(self.request, acc.user)
            if acc.user.is_superuser:
                messages.info(self.request,'Successfully login as admin '+ str(acc.user.username))
                return redirect("library:home")
            else:

                messages.info(self.request,'Successfully login as student '+ str(acc.user.username))
                return redirect("account:home")
        else:
            messages.info(self.request,"Your OTP code is wrong,Pls try another...")
            return HttpResponseRedirect(reverse("account:otp", kwargs={'phone':acc.phone_number}))

