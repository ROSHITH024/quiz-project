from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from quiz.models import Questions,Answers
from quizweb.form import UserRegistration,LoginForm,QuestionForm
from django.views.generic import View,TemplateView,CreateView,FormView,ListView
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
# Create your views here.

def signin_required(fn):
    def wraper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("sign--in")
        else:
            return fn(request,*args,**kw)
    return wraper

decs=[signin_required,never_cache]

class RegistrationForm(CreateView):
    template_name="register.html"
    model=User
    form_class=UserRegistration
    success_url=reverse_lazy("sign--in")
    
    # def get(self,request,*args,**kw):
    #     form=UserRegistration()
    #     return render(request,"register.html",{"form":form})

    def post(self,request,*args,**kw):
        form=UserRegistration(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,'Account Created')
            return redirect("signin")
        else:
            messages.error(request,'Error')
            return render(request,"register.html",{"form":form})

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

@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=QuestionForm
    success_url=reverse_lazy("house")
    model=Questions
    context_object_name="questions"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Questions.objects.exclude(user=self.request.user).order_by("-create_date")
    
    


def sign_out_view(request,*args,**kw):
    logout(request)
    return redirect("sign--in")

decs
def answer_view(request,*args,**kw):
    id=kw.get("id")
    ques=Questions.objects.get(id=id)
    ans=request.POST.get('answer')
    Answers.objects.create(question=ques,answer=ans,user=request.user)
    return redirect("house")

decs
def up_vote(request,*args,**kw):
    id=kw.get("id")
    ans=Answers.objects.get(id=id)
    ans.up_vote.add(request.user)
    return redirect("house")