from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

# Create your models here.

class Questions(models.Model):
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images",null=True)
    create_date=models.DateField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    @property
    def question_answers(self):
        qs=self.answers_set.all().annotate(u_count=Count('up_vote')).order_by('-u_count')
        return qs
    
    def __str__(self):
        return self.title

class Answers(models.Model):
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    answer=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    create_date=models.DateField(auto_now_add=True)
    up_vote=models.ManyToManyField(User,related_name="upvote")
    def __str__(self):
        return self.answer

    @property
    def votecount(self):
        return self.up_vote.all().count()


#  ans.up_vote.add(usr)    upvote cmd

