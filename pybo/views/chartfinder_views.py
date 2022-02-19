
import logging

from datetime import datetime, timedelta
from django.utils.dateformat import DateFormat

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from django.db.models import Avg
from django.db.models import F

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
    #ffinalcloseprice = request.GET.get('finalcloseprice', '0')

    temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]

    if kw and kw2:
        if kw[0:1] != 'A' and kw[0:1] != 'a':
            logger.info("주식명, 거래일 검색 시작")
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'ListedStockInfo').filter(StockName__iexact=kw).filter(trade_date=kw2)
        else:
            logger.info("주식코드, 거래일 검색 시작")
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'ListedStockInfo').all().filter(StockCode__icontains=kw).filter(trade_date=kw2).order_by('-trade_date')
    elif kw and kw2 == '':
        if kw[0:1] != 'A' and kw[0:1] != 'a':
            logger.info("주식명 검색 시작")
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'ListedStockInfo').filter(StockName__iexact=kw).order_by('-trade_date')[:500]
        else:
            logger.info("주식코드 검색 시작")
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'ListedStockInfo').all().filter(StockCode__icontains=kw).order_by('-trade_date')[:500]
    elif kw == '' and kw2:
        logger.info("거래일 검색 시작")
        stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'ListedStockInfo').all().filter(trade_date=kw2).order_by(F('ListedStockInfo__MarketCap').desc(nulls_last=True))[:500]
    else:
        logger.info("Default 검색 시작")

        temp_trade_date = timezone.now() - timedelta(days=410)
        temp_trade_date = DateFormat(temp_trade_date).format('Y-m-d')
        stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'ListedStockInfo').all().filter(StockCode='A005930').filter(trade_date__gt=temp_trade_date).order_by('trade_date')[:50]

    paginator = Paginator(stockbarcodedata_list, 10)
    page_obj = paginator.get_page(page)

    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))


    logger.info("stockbacktest View 끝")

    #context = {'stockbarcodedata_list':page_obj, 'page':page, 'kw2':kw2, 'kw':kw, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt, 'finalcloseprice':finalcloseprice  }
    context = {'stockbarcodedata_list':page_obj, 'page':page, 'kw2':kw2, 'kw':kw, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt  }

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
            pathdetailinfo_list = stockbarcodedata.objects.select_related('StockBarcodePerfTotal', 'ListedStockInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').all().filter(StockName__iexact=kw).filter(trade_date=kw2).order_by('-trade_date')
        else:
            logger.info("주식코드 검색 시작")
            pathdetailinfo_list = stockbarcodedata.objects.select_related('StockBarcodePerfTotal', 'ListedStockInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').all().filter(StockCode__icontains=kw).filter(trade_date=kw2).order_by('-trade_date')
    else:
        logger.info("Default 검색 시작")
        pathdetailinfo_list = stockbarcodedata.objects.select_related('StockBarcodePerfTotal', 'ListedStockInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').all().filter(StockCode__icontains='A005930').filter(trade_date=kw2).order_by('-trade_date')

    paginator = Paginator(pathdetailinfo_list, 10)
    page_obj = paginator.get_page(page)

    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))

    context = {'pathdetailinfo_list':page_obj, 'page': page, 'kw': kw, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt }

    logger.info("pathdetailinfo View 끝")

    return render(request, 'pybo/pathdetailinfo.html', context)


def investperfanaly(request):
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
            investperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'ForeignBuySellInfo').filter(trade_date=temp_trade_date).order_by(F('ForeignBuySellInfo__TradeAmount_NetBuy').asc(nulls_last=True))[:30]
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
        kw = "개인"
        kw2 = "순매수"

    paginator = Paginator(investperfanaly_list, 10)
    page_obj = paginator.get_page(page)

    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))


    logger.info("investperfanaly View 끝")

    context = {'investperfanaly_list':page_obj, 'page':page, 'kw':kw, 'kw2':kw2, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt }

    return render(request, 'pybo/investperfanaly.html', context)


def industryperfanaly(request):
    '''
     industryperfanaly 목록 출력
    '''

    logger.info("industryperfanaly View 시작")

    #입력 파라미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    kw2 = request.GET.get('kw2', '')

    totalvisitcnt = request.GET.get('totalvisitcnt', '0')
    todayvisitcnt = request.GET.get('todayvisitcnt', '0')

    temp_trade_date = timezone.now() - timedelta(days=8)
    temp_trade_date = DateFormat(temp_trade_date).format('Y-m-d')

    logger.info("업종 성과분석 검색시작")
    industryperfanaly_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal', 'ListedStockInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__IndustryType__iexact=kw).order_by(F('ListedStockInfo__MarketCap').desc(nulls_last=True))

    industryPER_Avg = stockbarcodedata.objects.select_related('ListedStockInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__IndustryType__iexact=kw).aggregate(PER=Avg('ListedStockInfo__PER'))
    industryPBR_Avg = stockbarcodedata.objects.select_related('ListedStockInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__IndustryType__iexact=kw).aggregate(PBR=Avg('ListedStockInfo__PBR'))
    industryDivRate_Avg = stockbarcodedata.objects.select_related('ListedStockInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__IndustryType__iexact=kw).aggregate(DivRate=Avg('ListedStockInfo__DivRate'))
    FinalPriceT1_Avg = stockbarcodedata.objects.select_related('ListedStockInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__IndustryType__iexact=kw).aggregate(FinalPriceT1=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT1')) / F('ListedStockInfo__FinalPriceT1') * 100))
    FinalPriceT7_Avg = stockbarcodedata.objects.select_related('ListedStockInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__IndustryType__iexact=kw).aggregate(FinalPriceT7=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT7')) / F('ListedStockInfo__FinalPriceT7') * 100))
    FinalPriceT30_Avg = stockbarcodedata.objects.select_related('ListedStockInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__IndustryType__iexact=kw).aggregate(FinalPriceT30=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT30')) / F('ListedStockInfo__FinalPriceT30') * 100))
    FinalPriceT90_Avg = stockbarcodedata.objects.select_related('ListedStockInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__IndustryType__iexact=kw).aggregate(FinalPriceT90=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT90')) / F('ListedStockInfo__FinalPriceT90') * 100))

    paginator = Paginator(industryperfanaly_list, 10)
    page_obj = paginator.get_page(page)

    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))


    logger.info("industryperfanaly View 끝")

    context = {'industryperfanaly_list':page_obj, 'page':page, 'kw':kw, 'kw2':kw2, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt, 'industryPER_Avg':industryPER_Avg, 'industryPBR_Avg':industryPBR_Avg, 'industryDivRate_Avg':industryDivRate_Avg, 'FinalPriceT1_Avg':FinalPriceT1_Avg, 'FinalPriceT7_Avg':FinalPriceT7_Avg, 'FinalPriceT30_Avg':FinalPriceT30_Avg, 'FinalPriceT90_Avg':FinalPriceT90_Avg }

    return render(request, 'pybo/industryperfanaly.html', context)

