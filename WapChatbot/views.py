from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from WapChatbot.models import Question, Choice
from django.urls import reverse
from django.utils import timezone

# 인덱스 페이지
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list':latest_question_list}
    return render(request, 'makesurvey.html', context)


# 투표하기 페이지, POST
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html',{
            'question':question,
            'error_message':"You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('tutorial:results',args=(question_id,)))


# 투표 생성
def makesurvey(request):
    question_subject = request.POST['question_subject']
    question_make_name = request.POST['question_make_name']
    question_overlap = request.POST['question_overlap']

    print(question_overlap)

    question_flag = True
    question_pub = request.POST['question_pub_date']
    q = Question(question_subject=question_subject, question_make_name=question_make_name,
                 question_flag = question_flag, question_pub = question_pub, pub_date=timezone.now())

    q.save()


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question})

