import logging

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from ..models import Question, StockBarcodeData

logger = logging.getLogger('pybo')


def chartfinder(request):
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

    return render(request, 'pybo/question_extralist.html', context)