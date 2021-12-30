import logging

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from ..models import stockbarcodedata, stockbarcodeperfreturn

logger = logging.getLogger('pybo')


def chartfinder(request):
    '''
     pybo 목록 출력
    '''

    logger.info("ChartFinder 레벨로 출력")

    #입력 파라미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    kw2 = request.GET.get('kw2', '')

    #stockbarcodedata_list = stockbarcodedata.objects.all().order_by('-trade_date')
    #stockbarperfreturn_list = stockbarcodeperfreturn.objects.select_related('StockBarcodeData').order_by('-trade_date')
    stockbarcodedata_list = stockbarcodedata.objects.all().order_by('-trade_date')

    if kw and kw2:
        stockbarcodedata_list = stockbarcodedata_list.filter(StockCode=kw).filter(trade_date=kw2)
    elif kw and kw2 == '':
        stockbarcodedata_list = stockbarcodedata_list.filter(StockCode=kw)
    elif kw=='' and kw2:
        stockbarcodedata_list = stockbarcodedata_list.filter(trade_date=kw2)

    paginator = Paginator(stockbarcodedata_list, 10)
    page_obj = paginator.get_page(page)

    context = {'stockbarcodedata_list':page_obj, 'page': page, 'kw2': kw2, 'kw': kw }
    #context = {'stockbarcodedata_list':question_list}

    return render(request, 'pybo/question_extralist.html', context)