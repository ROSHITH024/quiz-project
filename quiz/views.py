from django.shortcuts import render
# Create your views here.
from quiz.serializer import Userserializer,QuestionSerilizer,AnswerSerilizer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from quiz.models import Questions,Answers
from rest_framework import authentication,permissions
from rest_framework.decorators import action

class UsersViewSet(ModelViewSet):
    serializer_class=Userserializer
    queryset=User.objects.all()

class QuestionViewset(ModelViewSet):
    serializer_class=QuestionSerilizer
    queryset=Questions.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["GET"],detail=False)
    def my_questions(self,request,*args,**kw):
        qs=request.user.questions_set.all()
        sr=QuestionSerilizer(qs,many=True)
        return Response(data=sr.data)

    @action(methods=["POST"],detail=True)
    def add_answers(self,req,*args,**kw):
        id=kw.get("pk")
        usr=req.user
        ques=Questions.objects.get(id=id)
        sr=AnswerSerilizer(data=req.data,context={"question":ques,"user":usr})
        if sr.is_valid():
            sr.save()
            return Response(data=sr.data)
        else:
            return Response(sr.errors)

    @action(methods=["GET"],detail=True)
    def list_answers(self,req,*args,**kw):
        id=kw.get("pk")
        ques=Questions.objects.get(id=id)
        qs=ques.answers_set.all()
        sr=AnswerSerilizer(qs,many=True)
        return Response(data=sr.data)


class AnswerViewset(ModelViewSet):
    serializer_class=AnswerSerilizer
    queryset=Answers.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    @action(methods=["GET"],detail=True)
    def up_vote(self,req,*args,**kw):
        ans=self.get_object()
        usr=req.user
        ans.up_vote.add(usr)
        return Response(data="created")