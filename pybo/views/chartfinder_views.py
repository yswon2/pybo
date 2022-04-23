
import logging

from datetime import datetime, timedelta
from django.utils.dateformat import DateFormat

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Sum, Count
from django.db.models import Avg
from django.db.models import F

from ..models import stockbarcodedata, stockbarcodeperfreturn, stockbarcodeperftotal, listedstockinfo, PageViewCount, stockpriceinfo

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
    kw3 = request.GET.get('kw3', '')
    totalvisitcnt = request.GET.get('totalvisitcnt', '0')
    todayvisitcnt = request.GET.get('todayvisitcnt', '0')

    #temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]

    if kw and kw2:
        temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]

        if kw[0:1] != 'A' and kw[0:1] != 'a':
            logger.info("주식명, 거래일 검색 시작")

            if kw3 == '':
                stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'ListedStockInfo').filter(StockName__iexact=kw).filter(trade_date__gte=kw2).filter(trade_date__lte=kw2).order_by('-trade_date')
            else:
                stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'ListedStockInfo').filter(StockName__iexact=kw).filter(trade_date__gte=kw2).filter(trade_date__lte=kw3).order_by('-trade_date')

        else:
            logger.info("주식코드, 거래일 검색 시작")
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'ListedStockInfo').all().filter(StockCode__icontains=kw).filter(trade_date__gte=kw2).filter(trade_date__lte=kw3).order_by('-trade_date')
    elif kw and kw2 == '':
        temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]

        temp_trade_date = timezone.now() - timedelta(days=365)
        temp_trade_date = DateFormat(temp_trade_date).format('Y-m-d')

        temp_trade_date2 = timezone.now()
        temp_trade_date2 = DateFormat(temp_trade_date2).format('Y-m-d')

        if kw[0:1] != 'A' and kw[0:1] != 'a':
            logger.info("주식명 검색 시작")
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'ListedStockInfo').filter(StockName__iexact=kw).filter(trade_date__gte=temp_trade_date).filter(trade_date__lte=temp_trade_date2).order_by('-trade_date')
        else:
            logger.info("주식코드 검색 시작")
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'ListedStockInfo').all().filter(StockCode__icontains=kw).filter(trade_date__gte=temp_trade_date).filter(trade_date__lte=temp_trade_date2).order_by('-trade_date')
    elif kw == '' and kw2:
        logger.info("거래일 검색 시작")

        temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]
        temp_trade_date2 = timezone.now()
        temp_trade_date2 = DateFormat(temp_trade_date2).format('Y-m-d')
        if kw3 == '':
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'ListedStockInfo').all().filter(trade_date__gte=kw2).filter(trade_date__lte=temp_trade_date2).order_by(F('ListedStockInfo__MarketCap').desc(nulls_last=True))[:500]
        else:
            stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'ListedStockInfo').all().filter(trade_date__gte=kw2).filter(trade_date__lte=kw3).order_by(F('ListedStockInfo__MarketCap').desc(nulls_last=True))[:500]
    else:
        logger.info("Default 검색 시작")

        stockbarcodedata_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'ListedStockInfo').all().filter(StockCode='')

    paginator = Paginator(stockbarcodedata_list, 10)
    page_obj = paginator.get_page(page)

    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    #totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    #todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Count('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Count('view_count'))

    # 화면 조회 내역 기록 ==> 기간별 실현수익률 조회화면은 1000단위로 더해짐
    #ip = get_client_ip(request)
    #vc = PageViewCount.objects.get(ip=ip, create_date=viewdate)
    #if vc.view_count > 0:
    #    vc.view_count += 1000
    #else:
    #    vc.view_count = 1000
    #vc.save()

    ip = get_client_ip(request)
    createtime = timezone.now()
    cnt = PageViewCount.objects.filter(ip=ip, create_date=viewdate).count()
    if cnt == 0:
        vc = PageViewCount(ip=ip, create_date=viewdate, create_time=createtime)
        vc.save()
        vc.view_count = 1000
        vc.save()
    else:
        vc = PageViewCount.objects.get(ip=ip, create_date=viewdate)
        vc.view_count += 1000
        vc.save()


    logger.info("stockbacktest View 끝")

    context = {'stockbarcodedata_list':page_obj, 'page':page, 'kw2':kw2, 'kw3':kw3, 'kw':kw, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt  }

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

    totalvisitcnt = request.GET.get('totalvisitcnt', '0')
    todayvisitcnt = request.GET.get('todayvisitcnt', '0')

    if kw:
        temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]
        kw2 = request.GET.get('kw2', temp_trade_date)

        if (kw[0:1] != 'A' and kw[0:1] != 'a'):
            logger.info("주식명, 거래일 검색 시작")
            SelBarFinalCode = stockbarcodedata.objects.select_related('StockBarcodePerfReturn').filter(StockName__iexact=kw).filter(trade_date=kw2).values_list('BarFinalCode', flat=True).order_by('-trade_date')[:1]
            stockpathdetail_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(BarFinalCode__in=SelBarFinalCode).all().order_by('-trade_date', 'StockCode')
        else:
            logger.info("주식코드, 거래일 검색 시작")
            SelBarFinalCode = stockbarcodedata.objects.select_related('StockBarcodePerfReturn').filter(StockCode__icontains=kw).filter(trade_date=kw2).values_list('BarFinalCode', flat=True).order_by('-trade_date')[:1]
            stockpathdetail_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(BarFinalCode__in=SelBarFinalCode).all().order_by('-trade_date', 'StockCode')
    else:
        logger.info("Default 검색 시작")
        stockpathdetail_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(BarFinalCode__in='').all()
        #SelBarFinalCode = stockbarcodedata.objects.select_related('StockBarcodePerfReturn').filter(StockCode__icontains='A005930').filter(trade_date=kw2).values_list('BarFinalCode', flat=True).order_by('-trade_date')[:1]
        #stockpathdetail_list = stockbarcodedata.objects.select_related('StockBarcodePerfReturn', 'StockBarcodePerfTotal').all().filter(BarFinalCode__in=SelBarFinalCode).all().order_by('-trade_date')
    paginator = Paginator(stockpathdetail_list, 10)
    page_obj = paginator.get_page(page)

    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    #totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    #todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Count('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Count('view_count'))

    # 화면 조회 내역 기록 ==> 기술적지표 유사종목 조회화면은 100단위로 더해짐
    #ip = get_client_ip(request)
    #vc = PageViewCount.objects.get(ip=ip, create_date=viewdate)
    #if vc.view_count > 0:
    #    vc.view_count += 100
    #else:
    #    vc.view_count = 100
    #vc.save()

    ip = get_client_ip(request)
    createtime = timezone.now()
    cnt = PageViewCount.objects.filter(ip=ip, create_date=viewdate).count()
    if cnt == 0:
        vc = PageViewCount(ip=ip, create_date=viewdate, create_time=createtime)
        vc.save()
        vc.view_count = 100
        vc.save()
    else:
        vc = PageViewCount.objects.get(ip=ip, create_date=viewdate)
        vc.view_count += 100
        vc.save()

    logger.info("stockpathdetail View 끝")

    context = {'stockpathdetail_list':page_obj, 'page': page, 'kw': kw, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt }

    return render(request, 'pybo/stockpathdetail.html', context)




def pathdetailinfo(request):
    '''
     pathdetailinfo 목록 출력
    '''

    logger.info("pathdetailinfo View 시작")

    #입력 파라미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')

    #temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]
    #kw2 = request.GET.get('kw2', temp_trade_date)
    totalvisitcnt = request.GET.get('totalvisitcnt', '0')
    todayvisitcnt = request.GET.get('todayvisitcnt', '0')

    if kw:
        temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]
        kw2 = request.GET.get('kw2', temp_trade_date)

        if (kw[0:1] != 'A' and kw[0:1] != 'a'):
            logger.info("주식명 검색 시작")
            pathdetailinfo_list = stockbarcodedata.objects.select_related('StockBarcodePerfTotal', 'StockPriceInfo', 'ListedStockInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').all().filter(StockName__iexact=kw).filter(trade_date=kw2).order_by('-trade_date')
        else:
            logger.info("주식코드 검색 시작")
            pathdetailinfo_list = stockbarcodedata.objects.select_related('StockBarcodePerfTotal', 'StockPriceInfo', 'ListedStockInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').all().filter(StockCode__icontains=kw).filter(trade_date=kw2).order_by('-trade_date')
    else:
        logger.info("Default 검색 시작")
        pathdetailinfo_list = stockbarcodedata.objects.select_related('StockBarcodePerfTotal', 'StockPriceInfo', 'ListedStockInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').all().filter(StockCode__iexact='')
        #pathdetailinfo_list = stockbarcodedata.objects.select_related('StockBarcodePerfTotal', 'StockPriceInfo', 'ListedStockInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').all().filter(StockCode__iexact='').filter(trade_date=kw2).order_by('-trade_date')


    paginator = Paginator(pathdetailinfo_list, 10)
    page_obj = paginator.get_page(page)

    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    #totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    #todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Count('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Count('view_count'))

    # 화면 조회 내역 기록 ==> 기술적지표 상세조회 화면은 10단위로 더해짐
    #ip = get_client_ip(request)
    #vc = PageViewCount.objects.get(ip=ip, create_date=viewdate)
    #if vc.view_count > 0:
    #    vc.view_count += 10
    #else:
    #    vc.view_count = 10
    #vc.save()

    ip = get_client_ip(request)
    createtime = timezone.now()
    cnt = PageViewCount.objects.filter(ip=ip, create_date=viewdate).count()
    if cnt == 0:
        vc = PageViewCount(ip=ip, create_date=viewdate, create_time=createtime)
        vc.save()
        vc.view_count = 10
        vc.save()
    else:
        vc = PageViewCount.objects.get(ip=ip, create_date=viewdate)
        vc.view_count += 10
        vc.save()

    logger.info("pathdetailinfo View 끝")

    context = {'pathdetailinfo_list':page_obj, 'page': page, 'kw': kw, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt}

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

    if kw == '개인':

        temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]

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

        temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]

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

        temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]

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
        investperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'AntBuySellInfo').filter(trade_date='1900-01-01')[:1]
        #investperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'AntBuySellInfo').filter(trade_date=temp_trade_date).order_by(F('AntBuySellInfo__TradeAmount_NetBuy').desc(nulls_last=True))[:30]

    paginator = Paginator(investperfanaly_list, 10)
    page_obj = paginator.get_page(page)

    viewdate = DateFormat(timezone.now()).format('Y-m-d')
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

    ip = get_client_ip(request)
    createtime = timezone.now()
    cnt = PageViewCount.objects.filter(ip=ip, create_date=viewdate).count()
    if cnt == 0:
        vc = PageViewCount(ip=ip, create_date=viewdate, create_time=createtime)
        vc.save()
        vc.view_count = 10000
        vc.save()
    else:
        vc = PageViewCount.objects.get(ip=ip, create_date=viewdate)
        vc.view_count += 10000
        vc.save()

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

    #temp_trade_date = timezone.now() - timedelta(days=13)
    #temp_trade_date = DateFormat(temp_trade_date).format('Y-m-d')

    logger.info("업종 성과분석 검색시작")

    if kw and kw2 == '':
        logger.info("업종 검색시작")

        temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]
        industryperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__IndustryType__iexact=kw).order_by(F('ListedStockInfo__MarketCap').desc(nulls_last=True))
        industry_Avg = stockbarcodedata.objects.select_related('ListedStockInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__IndustryType__iexact=kw).aggregate(PER=Avg('ListedStockInfo__PER'), EPS=Avg('ListedStockInfo__EPS'), PBR=Avg('ListedStockInfo__PBR'), DivRate=Avg('ListedStockInfo__DivRate'), FinalPriceT1=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT1')) / F('ListedStockInfo__FinalPriceT1') * 100), FinalPriceT7=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT7')) / F('ListedStockInfo__FinalPriceT7') * 100), FinalPriceT30=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT30')) / F('ListedStockInfo__FinalPriceT30') * 100), FinalPriceT90=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT90')) / F('ListedStockInfo__FinalPriceT90') * 100))

    elif kw == '0' and kw2:
        logger.info("종목명 검색시작")

        temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]
        temp_IndustryType = listedstockinfo.objects.filter(StockName__iexact=kw2).values_list('IndustryType', flat=True).order_by('-IndustryType')[:1]
        industryperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__IndustryType=temp_IndustryType).order_by(F('ListedStockInfo__MarketCap').desc(nulls_last=True))
        industry_Avg = stockbarcodedata.objects.select_related('ListedStockInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__IndustryType=temp_IndustryType).aggregate(PER=Avg('ListedStockInfo__PER'), EPS=Avg('ListedStockInfo__EPS'), PBR=Avg('ListedStockInfo__PBR'), DivRate=Avg('ListedStockInfo__DivRate'), FinalPriceT1=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT1')) / F('ListedStockInfo__FinalPriceT1') * 100), FinalPriceT7=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT7')) / F('ListedStockInfo__FinalPriceT7') * 100), FinalPriceT30=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT30')) / F('ListedStockInfo__FinalPriceT30') * 100), FinalPriceT90=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT90')) / F('ListedStockInfo__FinalPriceT90') * 100))
    else:
        logger.info("Default 검색시작")

        industryperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').filter(trade_date='1900-01-01').filter(ListedStockInfo__IndustryType='업종')
        industry_Avg = stockbarcodedata.objects.select_related('ListedStockInfo').filter(trade_date='1900-01-01').filter(ListedStockInfo__IndustryType='업종').aggregate(PER=Avg('ListedStockInfo__PER'), EPS=Avg('ListedStockInfo__EPS'), PBR=Avg('ListedStockInfo__PBR'), DivRate=Avg('ListedStockInfo__DivRate'), FinalPriceT1=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT1')) / F('ListedStockInfo__FinalPriceT1') * 100), FinalPriceT7=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT7')) / F('ListedStockInfo__FinalPriceT7') * 100), FinalPriceT30=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT30')) / F('ListedStockInfo__FinalPriceT30') * 100), FinalPriceT90=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT90')) / F('ListedStockInfo__FinalPriceT90') * 100))

        #temp_IndustryType = listedstockinfo.objects.filter(StockName__iexact=kw2).values_list('IndustryType', flat=True).order_by('-IndustryType')[:1]
        #industryperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').filter(trade_date='1900-01-01').filter(ListedStockInfo__IndustryType=temp_IndustryType).order_by(F('ListedStockInfo__MarketCap').desc(nulls_last=True))
        #industry_Avg = stockbarcodedata.objects.select_related('ListedStockInfo').filter(trade_date='1900-01-01').filter(ListedStockInfo__IndustryType=temp_IndustryType).aggregate(PER=Avg('ListedStockInfo__PER'), EPS=Avg('ListedStockInfo__EPS'), PBR=Avg('ListedStockInfo__PBR'), DivRate=Avg('ListedStockInfo__DivRate'), FinalPriceT1=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT1')) / F('ListedStockInfo__FinalPriceT1') * 100), FinalPriceT7=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT7')) / F('ListedStockInfo__FinalPriceT7') * 100), FinalPriceT30=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT30')) / F('ListedStockInfo__FinalPriceT30') * 100), FinalPriceT90=Avg((F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT90')) / F('ListedStockInfo__FinalPriceT90') * 100))

    paginator = Paginator(industryperfanaly_list, 10)
    page_obj = paginator.get_page(page)

    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    #totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    #todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Count('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Count('view_count'))

    # 화면 조회 내역 기록 ==> 업종별 성과분석화면은 100000단위로 더해짐
    #ip = get_client_ip(request)
    #vc = PageViewCount.objects.get(ip=ip, create_date=viewdate)
    #if vc.view_count > 0:
    #    vc.view_count += 100000
    #else:
    #    vc.view_count = 100000
    #vc.save()

    ip = get_client_ip(request)
    createtime = timezone.now()
    cnt = PageViewCount.objects.filter(ip=ip, create_date=viewdate).count()
    if cnt == 0:
        vc = PageViewCount(ip=ip, create_date=viewdate, create_time=createtime)
        vc.save()
        vc.view_count = 100000
        vc.save()
    else:
        vc = PageViewCount.objects.get(ip=ip, create_date=viewdate)
        vc.view_count += 100000
        vc.save()



    logger.info("industryperfanaly View 끝")

    context = {'industryperfanaly_list':page_obj, 'page':page, 'kw':kw, 'kw2':kw2, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt, 'industry_Avg':industry_Avg}

    return render(request, 'pybo/industryperfanaly.html', context)



def stockperfanaly(request):
    '''
     stockperfanaly 목록 출력
    '''

    logger.info("stockperfanaly View 시작")

    #입력 파라미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    kw2 = request.GET.get('kw2', '')

    totalvisitcnt = request.GET.get('totalvisitcnt', '0')
    todayvisitcnt = request.GET.get('todayvisitcnt', '0')

    #kw = '수익률상위'
    #kw2 = '7일'


    logger.info("주식 수익률 검색시작")

    if kw == '수익률상위':
        temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]

        if kw2 == '7일':
            logger.info("수익률상위 7일 검색시작")
            stockperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'StockPriceInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__MarketCap__gt=100000000000).annotate(PriceT7Rtn=(F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT7')) / F('ListedStockInfo__FinalPriceT7') * 100).order_by(F('PriceT7Rtn').desc(nulls_last=True))[:20]
        elif kw2 == '30일':
            logger.info("수익률상위 30일 검색시작")
            stockperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'StockPriceInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__MarketCap__gt=100000000000).annotate(PriceT30Rtn=(F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT30')) / F('ListedStockInfo__FinalPriceT30') * 100).order_by(F('PriceT30Rtn').desc(nulls_last=True))[:20]
        elif kw2 == '90일':
            logger.info("수익률상위 90일 검색시작")
            stockperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'StockPriceInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__MarketCap__gt=100000000000).annotate(PriceT90Rtn=(F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT90')) / F('ListedStockInfo__FinalPriceT90') * 100).order_by(F('PriceT90Rtn').desc(nulls_last=True))[:20]

    elif kw == '수익률하위':
        temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]

        if kw2 == '7일':
            logger.info("수익률하위 7일 검색시작")
            stockperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'StockPriceInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__MarketCap__gt=100000000000).annotate(PriceT7Rtn=(F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT7')) / F('ListedStockInfo__FinalPriceT7') * 100).order_by(F('PriceT7Rtn').asc(nulls_last=True))[:20]
        elif kw2 == '30일':
            logger.info("수익률하위 30일 검색시작")
            stockperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'StockPriceInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__MarketCap__gt=100000000000).annotate(PriceT30Rtn=(F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT30')) / F('ListedStockInfo__FinalPriceT30') * 100).order_by(F('PriceT30Rtn').asc(nulls_last=True))[:20]
        elif kw2 == '90일':
            logger.info("수익률하위 90일 검색시작")
            stockperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'StockPriceInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').filter(trade_date=temp_trade_date).filter(ListedStockInfo__MarketCap__gt=100000000000).annotate(PriceT90Rtn=(F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT90')) / F('ListedStockInfo__FinalPriceT90') * 100).order_by(F('PriceT90Rtn').asc(nulls_last=True))[:20]
    else:
        logger.info("Default 검색시작")
        stockperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'StockPriceInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').filter(trade_date='1900-01-01').annotate(PriceT7Rtn=(F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT7')) / F('ListedStockInfo__FinalPriceT7') * 100)[:1]
        #stockperfanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'StockPriceInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').filter(trade_date='1900-01-01').filter(ListedStockInfo__MarketCap__gt=100000000000).annotate(PriceT7Rtn=(F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT7')) / F('ListedStockInfo__FinalPriceT7') * 100).order_by(F('PriceT7Rtn').desc(nulls_last=True))[:50]

    paginator = Paginator(stockperfanaly_list, 10)
    page_obj = paginator.get_page(page)

    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    #totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    #todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Count('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Count('view_count'))

    # 화면 조회 내역 기록 ==> 주식 상승하락율 조회화면은 1000000단위로 더해짐
    #ip = get_client_ip(request)
    #vc = PageViewCount.objects.get(ip=ip, create_date=viewdate)
    #if vc.view_count > 0:
    #    vc.view_count += 1000000
    #else:
    #    vc.view_count = 1000000
    #vc.save()

    ip = get_client_ip(request)
    createtime = timezone.now()
    cnt = PageViewCount.objects.filter(ip=ip, create_date=viewdate).count()
    if cnt == 0:
        vc = PageViewCount(ip=ip, create_date=viewdate, create_time=createtime)
        vc.save()
        vc.view_count = 1000000
        vc.save()
    else:
        vc = PageViewCount.objects.get(ip=ip, create_date=viewdate)
        vc.view_count += 1000000
        vc.save()

    logger.info("stockperfanaly View 끝")

    context = {'stockperfanaly_list':page_obj, 'page':page, 'kw':kw, 'kw2':kw2, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt}

    return render(request, 'pybo/stockperfanaly.html', context)





def stockshortsellanaly(request):
    '''
     stockshortsellanaly 목록 출력
    '''

    logger.info("stockperfanaly View 시작")

    #입력 파라미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    kw2 = request.GET.get('kw2', '')

    totalvisitcnt = request.GET.get('totalvisitcnt', '0')
    todayvisitcnt = request.GET.get('todayvisitcnt', '0')

    logger.info("공매도정보 검색시작")

    if kw != '':
        logger.info("종목검색시작")
        temp_trade_date = stockbarcodedata.objects.all().filter(StockCode='A005930').values_list('trade_date', flat=True).order_by('-trade_date')[:1]
        stockshortsellanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'StockPriceInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').filter(trade_date=temp_trade_date).filter(StockName__iexact=kw).annotate(PriceT7Rtn=(F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT7')) / F('ListedStockInfo__FinalPriceT7') * 100, PriceT30Rtn=(F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT30')) / F('ListedStockInfo__FinalPriceT30') * 100, PriceT90Rtn=(F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT90')) / F('ListedStockInfo__FinalPriceT90') * 100)
    else:
        logger.info("Default 검색시작")
        stockshortsellanaly_list = stockbarcodedata.objects.select_related('ListedStockInfo', 'StockPriceInfo', 'AntBuySellInfo', 'ForeignBuySellInfo', 'InstituteBuySellInfo').filter(trade_date='1900-01-01').annotate(PriceT7Rtn=(F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT7')) / F('ListedStockInfo__FinalPriceT7') * 100, PriceT30Rtn=(F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT30')) / F('ListedStockInfo__FinalPriceT30') * 100, PriceT90Rtn=(F('ListedStockInfo__FinalPriceT') - F('ListedStockInfo__FinalPriceT90')) / F('ListedStockInfo__FinalPriceT90') * 100)[:1]

    paginator = Paginator(stockshortsellanaly_list, 10)
    page_obj = paginator.get_page(page)

    viewdate = DateFormat(timezone.now()).format('Y-m-d')
    #totalvisitcnt = PageViewCount.objects.aggregate(view_count=Sum('view_count'))
    #todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Sum('view_count'))
    totalvisitcnt = PageViewCount.objects.aggregate(view_count=Count('view_count'))
    todayvisitcnt = PageViewCount.objects.filter(create_date=viewdate).aggregate(view_count=Count('view_count'))

    ip = get_client_ip(request)
    createtime = timezone.now()
    cnt = PageViewCount.objects.filter(ip=ip, create_date=viewdate).count()
    if cnt == 0:
        vc = PageViewCount(ip=ip, create_date=viewdate, create_time=createtime)
        vc.save()
        vc.view_count = 10000000
        vc.save()
    else:
        vc = PageViewCount.objects.get(ip=ip, create_date=viewdate)
        vc.view_count += 10000000
        vc.save()

    logger.info("stockshortsellanaly View 끝")

    context = {'stockshortsellanaly_list':page_obj, 'page':page, 'kw':kw, 'totalvisitcnt':totalvisitcnt, 'todayvisitcnt':todayvisitcnt}

    return render(request, 'pybo/stockshortsellanaly.html', context)






def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

