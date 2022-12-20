from rest_framework import serializers
from django.contrib.auth.models import User
from quiz.models import Questions,Answers

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["email","username","password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class AnswerSerilizer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    create_date=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    question=serializers.CharField(read_only=True)
    votecount=serializers.CharField(read_only=True)
    class Meta:
        model=Answers
        fields=[
            "id",
            "question",
            "answer",
            "user",
            "create_date",
            "votecount",
        ]

    def create(self, validated_data):
        ques=self.context.get("question")
        usr=self.context.get("user")
        return ques.answers_set.create(user=usr,**validated_data)

class QuestionSerilizer(serializers.ModelSerializer):
    create_date=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    id=serializers.CharField(read_only=True)
    question_answers=AnswerSerilizer(read_only=True,many=True)
    class Meta:
        model=Questions
        fields=[
            "id",
            "title",
            "description",
            "image",
            "user",
            "create_date",
            "question_answers",
        ]
