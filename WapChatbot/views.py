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
    if request.method == 'POST':
        question_subject = request.POST['question_subject']
        question_info = request.POST['question_info']
        question_make_name = request.POST['question_make_name']
        question_flag = False
        question_choices= request.POST['choice_items']

        question_overlap = False
        if 'question_overlap' in request.POST:
            question_overlap = True

        print(question_overlap, question_subject)

        q = Question(question_subject=question_subject,
                     question_make_name=question_make_name,
                     question_info=question_info,
                     question_pub_date=timezone.now(),
                     question_flag=question_flag,
                     question_overlap=question_overlap)

        q.save()

        for choice_index in range(1,len(question_choices)):
            c = Choice(question=q, choice_text=question_choices[choice_index], votes=0,votes_names="")
            c.save()

        return HttpResponseRedirect(reverse('onsurvey'))
    else:
        return render(request, 'makesurvey.html')


def endsurvey(request):
    return render(request, 'endsurvey.html')


def onsurvey(request):
    question_list = Question.objects.order_by('-question_pub_date')

    show_question_list = []
    for question in question_list:
        if question.question_flag is False and len(show_question_list) < 10:
            show_question_list.append(question)

    context = {'question_list':show_question_list}

    return render(request, 'onsurvey.html',context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question})

