import logging

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils.dateformat import DateFormat
from django.utils import timezone
from django.db.models import Sum, Count
from django.db.models import F

from datetime import datetime, timedelta
from ..models import Question, QuestionCount
from ..models import stockbarcodedata, stockbarcodeperfreturn, stockbarcodeperftotal, PageViewCount, listedstockinfo, stockpriceinfo

logger = logging.getLogger('pybo')


def index(request):
    '''
      investperfanaly 목록 출력
     '''

    logger.info("investperfanaly View 시작")

    #입력 파라미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    kw2 = request.GET.get('kw2', '')

    totalvisitcnt = request.GET.get('totalvisitcnt', '0')
    todayvisitcnt = request.GET.get('todayvisitcnt', '0')

    temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]

    if kw == '개인':
        if kw2 == '순매수':
            logger.info("개인 순매수 검색시작")
            investperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'AntBuySellInfo').filter(trade_date=temp_trade_date).order_by(F('AntBuySellInfo__TradeAmount_NetBuy').desc(nulls_last=True))[:30]
            kw = "개인"
            kw2 = "순매수"
        else:
            logger.info("개인 순매도  검색시작")
            investperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'AntBuySellInfo').filter(trade_date=temp_trade_date).order_by(F('AntBuySellInfo__TradeAmount_NetBuy').asc(nulls_last=True))[:30]
            kw = "개인"
            kw2 = "순매도"
    elif kw == '외국인':
        if kw2 == '순매수':
            logger.info("외국인 순매수 검색시작")
            investperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'ForeignBuySellInfo').filter(trade_date=temp_trade_date).order_by(F('ForeignBuySellInfo__TradeAmount_NetBuy').desc(nulls_last=True))[:30]
            kw = "외국인"
            kw2 = "순매수"
        else:
            logger.info("외국인 순매도 검색시작")
            investperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'ForeignBuySellInfo').filter(trade_date=temp_trade_date).order_by(F('ForeignBuySellInfo__TradeAmount_NetBuy').asc())[:30]
            kw = "외국인"
            kw2 = "순매도"
    elif kw == '기관':
        if kw2 == '순매수':
            logger.info("기관 순매수 검색시작")
            investperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'InstituteBuySellInfo').filter(trade_date=temp_trade_date).order_by(F('InstituteBuySellInfo__TradeAmount_NetBuy').desc(nulls_last=True))[:30]
            kw = "기관"
            kw2 = "순매수"
        else:
            logger.info("기관 순매도 검색시작")
            investperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'InstituteBuySellInfo').filter(trade_date=temp_trade_date).order_by(F('InstituteBuySellInfo__TradeAmount_NetBuy').asc(nulls_last=True))[:30]
            kw = "기관"
            kw2 = "순매도"
    else:
        logger.info("Default 개인 순매수 검색시작")
        investperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'AntBuySellInfo').filter(trade_date=temp_trade_date).order_by(F('AntBuySellInfo__TradeAmount_NetBuy').desc(nulls_last=True))[:30]
        #kw = "개인"
        #kw2 = "순매수"

    paginator = Paginator(investperfanaly_list, 10)
    page_obj = paginator.get_page(page)


    ip = get_client_ip(request)
    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    createtime = timezone.now()
    cnt = PageViewCount.objects.filter(ip=ip, create_date=viewdate).count()
    if cnt == 0:
        vc = PageViewCount(ip=ip, create_date=viewdate, create_time=createtime)
        vc.save()
        if vc.view_count:
            vc.view_count += 10000
        else:
            vc.view_count = 10000
        vc.save()

    #totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    #todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Count('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Count('view_count'))

    # 화면 조회 내역 기록 ==> 거래주체별 성과분석화면은 10000단위로 더해짐
    #ip = get_client_ip(request)
    #vc = PageViewCount.objects.get(ip=ip, create_date=viewdate)
    #if vc.view_count > 0:
    #    vc.view_count += 10000
    #else:
    #    vc.view_count = 10000
    #vc.save()

    logger.info("investperfanaly View 끝")

    context = {'investperfanaly_list':page_obj, 'page':page, 'kw':kw, 'kw2':kw2, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt }

    return render(request, 'pybo/investperfanaly.html', context)



'''
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

    # 화면 조회 내역 기록 ==> 자유게시판 조회화면은 1단위로 더해짐
    ip = get_client_ip(request)
    vc = PageViewCount.objects.get(ip=ip, create_date=viewdate)
    if vc.view_count > 0:
        vc.view_count += 1
    else:
        vc.view_count = 1
    vc.save()


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

