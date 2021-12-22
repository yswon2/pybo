import logging

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from ..models import Question

logger = logging.getLogger('pybo')

def index(request):
    '''
     pybo 목록 출력
    '''

    logger.info("INFO 레벨로 출력")

    #입력 파라미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')

    question_list = Question.objects.order_by('-create_date')
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

    return render(request, 'pybo/question_detail.html', context)


def extra(request):
    '''
     pybo 목록 출력
    '''

    logger.info("EXTRA INFO 레벨로 출력")

    #입력 파라미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', 'yswon2')

    question_extralist = Question.objects.order_by('-create_date')
    if kw:
        question_extralist = question_extralist.filter(
            Q(author__username__icontains=kw)
        ).distinct()

    paginator = Paginator(question_extralist, 10)
    page_obj = paginator.get_page(page)

    context = {'question_extralist':page_obj, 'page': page, 'kw': kw}

    return render(request, 'pybo/question_extralist.html', context)
