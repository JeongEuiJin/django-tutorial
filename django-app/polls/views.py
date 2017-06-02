from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse

from polls.models import Question, Choice


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    latest_question_list = get_list_or_404(Question.objects.order_by('-pub_date')[:5])
    context = {
        'latest_question_list': latest_question_list,
    }
    # 이것을 사용하기위해서는 settings.py에서 TEMPLATE_DIR 을 추가해준다
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # question.choice_set.
    # Choice.objects.filter(question=question) 두개는 같은 문구이다
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoseNotExist as e:
    #     raise Http404('Question does not exist')
    context = {
        'question': question
    }


    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    context = {
        'question':question
    }

    return render(request,'polls:results',context)


def vote(request, question_id):
    if request.method == 'POST':
        data = request.POST
        try:
            choice_id = data['choice']
            choice = Choice.objects.get(id=choice_id)
            choice.votes += 1
            choice.save()
            return redirect('polls:results', question_id)
        except (KeyError, Choice.DoesNotExist):
            messages.add_message(request, messages.ERROR, "you didn't select a choice")
            return redirect('polls:detail', question_id)
    else:
        return HttpResponse("you're voting on question %s" % question_id)
