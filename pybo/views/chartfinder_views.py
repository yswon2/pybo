
import logging

from datetime import datetime
from django.utils.dateformat import DateFormat

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from ..models import stockbarcodedata, stockbarcodeperfreturn, stockbarcodeperftotal

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

    if kw and kw2:
        if kw[0:1] != 'A' and kw[0:1] != 'a':
            logger.info("주식명, 거래일 검색 시작")
            #stockbarcodedata_list = stockbarcodedata.objects.filter(StockName__icontains=kw).filter(trade_date=kw2).order_by('trade_date')
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').filter(StockName__icontains=kw).filter(trade_date=kw2)
        else:
            logger.info("주식코드, 거래일 검색 시작")
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(StockCode__icontains=kw).filter(trade_date=kw2).order_by('-trade_date')
    elif kw and kw2 == '':
        if kw[0:1] != 'A' and kw[0:1] != 'a':
            logger.info("주식명 검색 시작")
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').filter(StockName__icontains=kw).order_by('-trade_date')
            #stockbarcodedata_list = stockbarcodedata.objects.filter(StockName__icontains=kw).order_by('trade_date')
        else:
            logger.info("주식코드 검색 시작")
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(StockCode__icontains=kw).order_by('-trade_date')
    elif kw == '' and kw2:
        logger.info("거래일 검색 시작")
        stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(trade_date=kw2).order_by('StockCode')
    else:
        logger.info("Default 검색 시작")
        #temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]
        #kw2 = request.GET.get('kw2', temp_trade_date)
        stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(StockCode='A005930').order_by('-trade_date')[:50]

    paginator = Paginator(stockbarcodedata_list, 10)
    page_obj = paginator.get_page(page)

    logger.info("stockbacktest View 끝")

    context = {'stockbarcodedata_list':page_obj, 'page': page, 'kw2': kw2, 'kw': kw }

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

    if kw:
        if (kw[0:1] != 'A' and kw[0:1] != 'a'):
            logger.info("주식명, 거래일 검색 시작")
            SelBarFinalCode = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').filter(StockName__icontains=kw).filter(trade_date=kw2).values_list('BarFinalCode', flat=True).order_by('-trade_date')[:1]
            stockpathdetail_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(BarFinalCode__in=SelBarFinalCode).all().order_by('-trade_date')
        else:
            logger.info("주식코드, 거래일 검색 시작")
            SelBarFinalCode = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(StockCode__icontains=kw).filter(trade_date=kw2).values_list('BarFinalCode', flat=True).order_by('-trade_date')
            stockpathdetail_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(BarFinalCode__in=SelBarFinalCode).all().order_by('-trade_date')
    else:
        logger.info("Default 검색 시작")
        stockpathdetail_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(BarFinalCode__in='').all()

    paginator = Paginator(stockpathdetail_list, 10)
    page_obj = paginator.get_page(page)

    context = {'stockpathdetail_list':page_obj, 'page': page, 'kw': kw }

    logger.info("stockpathdetail View 끝")

    return render(request, 'pybo/stockpathdetail.html', context)