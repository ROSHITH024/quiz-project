from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from quiz.models import Questions,Answers
from quizweb.form import UserRegistration,LoginForm
from django.views.generic import View,TemplateView,CreateView,FormView
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy

# Create your views here.

class RegistrationForm(CreateView):
    template_name="register.html"
    model=User
    form_class=UserRegistration
    success_url=reverse_lazy("sign--in")
    
    # def get(self,request,*args,**kw):
    #     form=UserRegistration()
    #     return render(request,"register.html",{"form":form})

    # def post(self,request,*args,**kw):
    #     form=UserRegistration(request.POST)
    #     if form.is_valid():
    #         User.objects.create_user(**form.cleaned_data)
    #         messages.success(request,'Account Created')
    #         return redirect("signin")
    #     else:
    #         messages.error(request,'Error')
    #         return render(request,"register.html",{"form":form})

class UserLoginForm(FormView):
    template_name="login.html"
    form_class=LoginForm
    # def get(self,request,*args,**kw):
    #     form=LoginForm()
    #     return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            # print(f"user={usr}")
            if usr:
                login(request,usr)
                return redirect("house")
            else:
                return redirect("sign--in")

class IndexView(TemplateView):
    template_name="index.html"


def sign_out_view(request,*args,**kw):
    logout(request)
    return redirect("sign--in")