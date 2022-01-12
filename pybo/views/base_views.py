import logging

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils.dateformat import DateFormat
from django.utils import timezone

from ..models import Question, QuestionCount

logger = logging.getLogger('pybo')


def index(request):
    '''
     pybo 목록 출력
    '''

    logger.info("INFO 레벨로 출력")

    #입력 파라미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')

    question_list = Question.objects.order_by('-notice', '-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list':page_obj, 'page': page, 'kw': kw}
    #context = {'question_list':question_list}

    return render(request, 'pybo/question_list.html', context)



def detail(request, question_id):
    """
    내용출력
    """
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}

    ip = get_client_ip(request)
    cnt = QuestionCount.objects.filter(ip=ip, question=question).count()
    if cnt == 0:
        qc = QuestionCount(ip=ip, question=question)
        qc.save()
        if question.view_count:
            question.view_count += 1
        else:
            question.view_count = 1
        question.save()

    return render(request, 'pybo/question_detail.html', context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

