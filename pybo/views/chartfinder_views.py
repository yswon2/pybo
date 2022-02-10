
import logging

from datetime import datetime, timedelta
from django.utils.dateformat import DateFormat

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Sum

from ..models import stockbarcodedata, stockbarcodeperfreturn, stockbarcodeperftotal, listedstockinfo, PageViewCount

logger = logging.getLogger('pybo')


def stockbacktest(request):
    '''
     stockbacktest 목록 출력
    '''

    logger.info("stockbacktest View 시작")

    #입력 파라미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    kw2 = request.GET.get('kw2', '')
    #kw2 = request.GET.get('kw2', DateFormat(datetime.now()).format('Y-m-d'))
    totalvisitcnt = request.GET.get('totalvisitcnt', '0')
    todayvisitcnt = request.GET.get('todayvisitcnt', '0')
    finalcloseprice = request.GET.get('finalcloseprice', '0')

    temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]

    if kw and kw2:
        if kw[0:1] != 'A' and kw[0:1] != 'a':
            logger.info("주식명, 거래일 검색 시작")
            finalcloseprice = stockbarcodedata.objects.filter(StockName__iexact=kw).filter(trade_date=temp_trade_date).aggregate(ClosePrice=Sum('ClosePrice'))
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').filter(StockName__iexact=kw).filter(trade_date=kw2)
        else:
            logger.info("주식코드, 거래일 검색 시작")
            finalcloseprice = stockbarcodedata.objects.filter(StockCode__icontains=kw).filter(trade_date=temp_trade_date).aggregate(ClosePrice=Sum('ClosePrice'))
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(StockCode__icontains=kw).filter(trade_date=kw2).order_by('-trade_date')
    elif kw and kw2 == '':
        if kw[0:1] != 'A' and kw[0:1] != 'a':
            logger.info("주식명 검색 시작")
            finalcloseprice = stockbarcodedata.objects.filter(StockName__iexact=kw).filter(trade_date=temp_trade_date).aggregate(ClosePrice=Sum('ClosePrice'))
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').filter(StockName__iexact=kw).order_by('-trade_date')[:500]
        else:
            logger.info("주식코드 검색 시작")
            finalcloseprice = stockbarcodedata.objects.filter(StockCode__icontains=kw).filter(trade_date=temp_trade_date).aggregate(ClosePrice=Sum('ClosePrice'))
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(StockCode__icontains=kw).order_by('-trade_date')[:500]
    elif kw == '' and kw2:
        logger.info("거래일 검색 시작")
        finalcloseprice = stockbarcodedata.objects.filter(trade_date=temp_trade_date).values_list('ClosePrice', flat=True)
        stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal', 'ListedStockInfo').all().filter(trade_date=kw2).order_by('-ListedStockInfo__MarketCap')[:500]
    else:
        logger.info("Default 검색 시작")

        finalcloseprice = stockbarcodedata.objects.filter(StockCode__icontains='A005930').filter(trade_date=temp_trade_date).aggregate(ClosePrice=Sum('ClosePrice'))
        temp_trade_date = timezone.now() - timedelta(days=410)
        temp_trade_date = DateFormat(temp_trade_date).format('Y-m-d')
        stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(StockCode='A005930').filter(trade_date__gt=temp_trade_date).order_by('trade_date')[:50]

    paginator = Paginator(stockbarcodedata_list, 10)
    page_obj = paginator.get_page(page)

    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))


    logger.info("stockbacktest View 끝")

    context = {'stockbarcodedata_list':page_obj, 'page':page, 'kw2':kw2, 'kw':kw, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt, 'finalcloseprice':finalcloseprice  }

    return render(request, 'pybo/question_extralist.html', context)



def stockpathdetail(request):
    '''
     stockpathdetail 목록 출력
    '''

    logger.info("stockpathdetail View 시작")

    #입력 파라미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    #kw2 = request.GET.get('kw2', DateFormat(datetime.now()).format('Y-m-d'))

    temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]
    kw2 = request.GET.get('kw2', temp_trade_date)
    totalvisitcnt = request.GET.get('totalvisitcnt', '0')
    todayvisitcnt = request.GET.get('todayvisitcnt', '0')

    if kw:
        if (kw[0:1] != 'A' and kw[0:1] != 'a'):
            logger.info("주식명, 거래일 검색 시작")
            SelBarFinalCode = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').filter(StockName__iexact=kw).filter(trade_date=kw2).values_list('BarFinalCode', flat=True).order_by('-trade_date')[:1]
            stockpathdetail_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(BarFinalCode__in=SelBarFinalCode).all().order_by('-trade_date', 'StockCode')
        else:
            logger.info("주식코드, 거래일 검색 시작")
            SelBarFinalCode = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(StockCode__icontains=kw).filter(trade_date=kw2).values_list('BarFinalCode', flat=True).order_by('-trade_date')[:1]
            stockpathdetail_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(BarFinalCode__in=SelBarFinalCode).all().order_by('-trade_date', 'StockCode')

    else:
        logger.info("Default 검색 시작")
        SelBarFinalCode = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(StockCode__icontains='A005930').filter(trade_date=kw2).values_list('BarFinalCode', flat=True).order_by('-trade_date')[:1]
        stockpathdetail_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(BarFinalCode__in=SelBarFinalCode).all().order_by('-trade_date')

    paginator = Paginator(stockpathdetail_list, 10)
    page_obj = paginator.get_page(page)

    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))

    context = {'stockpathdetail_list':page_obj, 'page': page, 'kw': kw, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt  }

    logger.info("stockpathdetail View 끝")

    return render(request, 'pybo/stockpathdetail.html', context)




def pathdetailinfo(request):
    '''
     pathdetailinfo 목록 출력
    '''

    logger.info("pathdetailinfo View 시작")

    #입력 파라미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')

    temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]
    kw2 = request.GET.get('kw2', temp_trade_date)
    totalvisitcnt = request.GET.get('totalvisitcnt', '0')
    todayvisitcnt = request.GET.get('todayvisitcnt', '0')

    if kw:
        if (kw[0:1] != 'A' and kw[0:1] != 'a'):
            logger.info("주식명 검색 시작")
            pathdetailinfo_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(StockName__iexact=kw).filter(trade_date=kw2).order_by('-trade_date')
        else:
            logger.info("주식코드 검색 시작")
            pathdetailinfo_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(StockCode__icontains=kw).filter(trade_date=kw2).order_by('-trade_date')
    else:
        logger.info("Default 검색 시작")
        #pathdetailinfo_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(StockCode__in='').all()
        pathdetailinfo_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(StockCode__icontains='A005930').filter(trade_date=kw2).all()

    paginator = Paginator(pathdetailinfo_list, 10)
    page_obj = paginator.get_page(page)

    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))

    context = {'pathdetailinfo_list':page_obj, 'page': page, 'kw': kw, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt  }

    logger.info("pathdetailinfo View 끝")

    return render(request, 'pybo/pathdetailinfo.html', context)


