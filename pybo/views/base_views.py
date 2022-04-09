import logging

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils.dateformat import DateFormat
from django.utils import timezone
from django.db.models import Sum, Count

from datetime import datetime, timedelta
from ..models import Question, QuestionCount
from ..models import stockbarcodedata, stockbarcodeperfreturn, stockbarcodeperftotal, PageViewCount, listedstockinfo

logger = logging.getLogger('pybo')


def index(request):

    logger.info("INFO 레벨로 출력")

    #입력 파라미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    totalvisitcnt = request.GET.get('totalvisitcnt', '0')
    todayvisitcnt = request.GET.get('todayvisitcnt', '0')

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

    ip = get_client_ip(request)
    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    createtime = timezone.now()
    cnt = PageViewCount.objects.filter(ip=ip, create_date=viewdate).count()
    if cnt == 0:
        vc = PageViewCount(ip=ip, create_date=viewdate, create_time=createtime)
        vc.save()
        if vc.view_count:
            vc.view_count += 1
        else:
            vc.view_count = 1
        vc.save()

    #totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    #todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Count('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Count('view_count'))

    context = {'question_list':page_obj, 'page': page, 'kw': kw, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt }
    #context = {'question_list':question_list}

    return render(request, 'pybo/question_list.html', context)

    '''
     pathdetailinfo 목록 출력
    '''
'''
    logger.info("pathdetailinfo View 시작")

    #입력 파라미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    totalvisitcnt = request.GET.get('totalvisitcnt', '0')
    todayvisitcnt = request.GET.get('todayvisitcnt', '0')

    temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]
    kw2 = request.GET.get('kw2', temp_trade_date)

    if kw:
        if (kw[0:1] != 'A' and kw[0:1] != 'a'):
            logger.info("주식명 검색 시작")
            pathdetailinfo_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal', 'ListedStockInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').all().filter(StockName__iexact=kw).filter(trade_date=kw2).order_by('-trade_date')
        else:
            logger.info("주식코드 검색 시작")
            pathdetailinfo_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal', 'ListedStockInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').all().filter(StockCode__icontains=kw).filter(trade_date=kw2).order_by('-trade_date')
    else:
        logger.info("Default 검색 시작")
        pathdetailinfo_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal', 'ListedStockInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').all().filter(StockCode__icontains='A005930').filter(trade_date=kw2)

    #paginator = Paginator(pathdetailinfo_list, 10)
    #page_obj = paginator.get_page(page)

    ip = get_client_ip(request)
    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    createtime = timezone.now()
    cnt = PageViewCount.objects.filter(ip=ip, create_date=viewdate).count()
    if cnt == 0:
        vc = PageViewCount(ip=ip, create_date=viewdate, create_time=createtime)
        vc.save()
        if vc.view_count:
            vc.view_count += 1
        else:
            vc.view_count = 1
        vc.save()

    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))

    #context = {'pathdetailinfo_list':page_obj, 'page': page, 'kw': kw }
    context = {'pathdetailinfo_list':pathdetailinfo_list, 'kw': kw, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt }


    logger.info("pathdetailinfo View 끝")

    return render(request, 'pybo/pathdetailinfo.html', context)
'''



def qna(request):
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

    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Count('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Count('view_count'))
    #totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    #todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))

    context = {'question_list':page_obj, 'page': page, 'kw': kw, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt}

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

