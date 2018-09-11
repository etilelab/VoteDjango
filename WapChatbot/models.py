from django.db import models

# Create your models here.


# 투표 관련 테이블
class Question(models.Model):
    question_text = models.CharField(max_length=300) # 투표 제목
    question_make_name = models.CharField(max_length=100) # 투표 생성자 이름
    question_flag = models.BooleanField(default=True) # 투표 종료 여부
    pub_date = models.DateTimeField('date published') # 투표 생성일

    def __str__(self):
        return self.question_text


# 투표 항목 테이블
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # 투표 외래키 설정
    choice_text = models.CharField(max_length=200) # 투표 항목
    votes = models.IntegerField(default=0) # 투표 횟수


    def __str__(self):
        return self.choice_text
