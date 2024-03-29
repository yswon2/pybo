from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    view_count = models.IntegerField(default=0)
    notice = models.CharField(max_length=1, default='N')  # 공지사항 여부

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)


class QuestionCount(models.Model):
    ip = models.CharField(max_length=30)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.ip



class PageViewCount(models.Model):
    ip = models.CharField(max_length=30)
    create_date = models.DateField(null=False, blank=False)
    create_time = models.DateTimeField(null=True, blank=True)
    view_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.ip

class stockbarcodeperfreturn(models.Model):

    trade_date = models.DateField(null=False, blank=False)
    StockCode = models.CharField(null=False, blank=False,  max_length=20)
    StockName = models.CharField(null=True, blank=True, max_length=100)
    MarketType = models.CharField(null=False, blank=False, max_length=15)
    ClosePrice = models.FloatField()
    BarFinalCode = models.CharField(null=True, blank=True, max_length=20)
    BarFinalCodeDtl = models.CharField(null=True, blank=True, max_length=20)
    Day1PL = models.FloatField()
    Day1Return = models.FloatField()
    ClosePriceAft1 = models.FloatField()
    Day7PL = models.FloatField()
    Day7Return = models.FloatField()
    ClosePriceAft7 = models.FloatField()
    Day30PL = models.FloatField()
    Day30Return = models.FloatField()
    ClosePriceAft30 = models.FloatField()
    Day90PL = models.FloatField()
    Day90Return = models.FloatField()
    ClosePriceAft90 = models.FloatField()
    Day180PL = models.FloatField()
    Day180Return = models.FloatField()
    ClosePriceAft180 = models.FloatField()
    Day360PL = models.FloatField()
    Day360Return = models.FloatField()
    ClosePriceAft360 = models.FloatField()
    TodayPL = models.FloatField(null=True,)
    TodayReturn = models.FloatField(null=True)

    StockBarcode_ID = models.CharField(null=False, blank=False, primary_key=True, max_length=150, default='')



class stockbarcodeperftotal(models.Model):

    BarFinalCode = models.CharField(null=False, blank=False, primary_key=True, max_length=20)
    MarketType = models.CharField(null=False, blank=False, max_length=15)
    TotDay1Return = models.FloatField()
    TotDay7Return = models.FloatField()
    TotDay30Return = models.FloatField()
    TotDay90Return = models.FloatField()
    TotDay180Return = models.FloatField()
    TotDay360Return = models.FloatField()
    BarFinalCode_Cnt = models.IntegerField()
    TotDay1Average = models.FloatField()
    TotDay7Average = models.FloatField()
    TotDay30Average = models.FloatField()
    TotDay90Average = models.FloatField()
    TotDay180Average = models.FloatField()
    TotDay360Average = models.FloatField()
    PlusTotDay1Return = models.FloatField()
    MinusTotDay1Return = models.FloatField()
    PlusTotDay7Return = models.FloatField()
    MinusTotDay7Return = models.FloatField()
    PlusTotDay30Return = models.FloatField()
    MinusTotDay30Return = models.FloatField()
    PlusTotDay90Return = models.FloatField()
    MinusTotDay90Return = models.FloatField()
    PlusTotDay180Return = models.FloatField()
    MinusTotDay180Return = models.FloatField()
    PlusTotDay360Return = models.FloatField()
    MinusTotDay360Return = models.FloatField()
    PlusDay1BarCode_Cnt = models.IntegerField()
    MinusDay1BarCode_Cnt = models.IntegerField()
    PlusDay7BarCode_Cnt = models.IntegerField()
    MinusDay7BarCode_Cnt = models.IntegerField()
    PlusDay30BarCode_Cnt = models.IntegerField()
    MinusDay30BarCode_Cnt = models.IntegerField()
    PlusDay90BarCode_Cnt = models.IntegerField()
    MinusDay90BarCode_Cnt = models.IntegerField()
    PlusDay180BarCode_Cnt = models.IntegerField()
    MinusDay180BarCode_Cnt = models.IntegerField()
    PlusDay360BarCode_Cnt = models.IntegerField()
    MinusDay360BarCode_Cnt = models.IntegerField()
    PlusTotDay1Average = models.FloatField()
    MinusTotDay1Average = models.FloatField()
    PlusTotDay7Average = models.FloatField()
    MinusTotDay7Average = models.FloatField()
    PlusTotDay30Average = models.FloatField()
    MinusTotDay30Average = models.FloatField()
    PlusTotDay90Average = models.FloatField()
    MinusTotDay90Average = models.FloatField()
    PlusTotDay180Average = models.FloatField()
    MinusTotDay180Average = models.FloatField()
    PlusTotDay360Average = models.FloatField()
    MinusTotDay360Average = models.FloatField()
    TotDay7MaxReturn = models.FloatField()
    TotDay30MaxReturn = models.FloatField()
    TotDay90MaxReturn = models.FloatField()
    TotDay180MaxReturn = models.FloatField()
    TotDay360MaxReturn = models.FloatField()
    TotDay7MinReturn = models.FloatField()
    TotDay30MinReturn = models.FloatField()
    TotDay90MinReturn = models.FloatField()
    TotDay180MinReturn = models.FloatField()
    TotDay360MinReturn = models.FloatField()
    Day7SuccessRate = models.FloatField()
    Day30SuccessRate = models.FloatField()
    Day1SuccessRate = models.FloatField()


class listedstockinfo(models.Model):

    StockCode = models.CharField(null=False, blank=False, primary_key=True, max_length=20)
    StockName = models.CharField(null=True, blank=True, max_length=100)
    MarketType = models.CharField(null=True, blank=True, max_length=15)
    MarketTypeDetail = models.CharField(null=True, blank=True, max_length=15)
    MarketCap = models.FloatField()
    StockNum = models.FloatField()
    FinalPriceT = models.FloatField(default=0)
    FinalPriceT1 = models.FloatField(default=0)
    FinalPriceT7 = models.FloatField(default=0)
    FinalPriceT30 = models.FloatField(default=0)
    FinalPriceT90 = models.FloatField(default=0)
    EPS = models.FloatField(default=0)
    PER = models.FloatField(default=0)
    Forward_EPS = models.FloatField(default=0)
    Forward_PER = models.FloatField(default=0)
    BPS = models.FloatField(default=0)
    PBR = models.FloatField(default=0)
    DivAmount = models.FloatField(default=0)
    DivRate = models.FloatField(default=0)
    IndustryType = models.CharField(null=True, blank=True, max_length=15)

    ForeignStockNo = models.FloatField(default=0)
    ForeignStockRate = models.FloatField(default=0)
    ShortSellRate = models.FloatField(default=0)
    ShortSellNum = models.FloatField(default=0)
    ShortSellAmont = models.FloatField(default=0)

    TodayShortTradeNum = models.FloatField(default=0)
    TodayShortTradeAmount = models.FloatField(default=0)
    TodayTotalTradeAmount = models.FloatField(default=0)
    TodayShortTradeRate = models.FloatField(default=0)


class AntBuySellInfo(models.Model):

    StockCode = models.CharField(null=False, blank=False, primary_key=True, max_length=20)
    StockName = models.CharField(null=True, blank=True, max_length=100)
    TradeVolume_Sell = models.FloatField(default=0)
    TradeVolume_Buy = models.FloatField(default=0)
    TradeVolume_NetBuy = models.FloatField(default=0)
    TradeAmount_Sell = models.FloatField(default=0)
    TradeAmount_Buy = models.FloatField(default=0)
    TradeAmount_NetBuy = models.FloatField(default=0)


class ForeignBuySellInfo(models.Model):

    StockCode = models.CharField(null=False, blank=False, primary_key=True, max_length=20)
    StockName = models.CharField(null=True, blank=True, max_length=100)
    TradeVolume_Sell = models.FloatField(default=0)
    TradeVolume_Buy = models.FloatField(default=0)
    TradeVolume_NetBuy = models.FloatField(default=0)
    TradeAmount_Sell = models.FloatField(default=0)
    TradeAmount_Buy = models.FloatField(default=0)
    TradeAmount_NetBuy = models.FloatField(default=0)


class InstituteBuySellInfo(models.Model):

    StockCode = models.CharField(null=False, blank=False, primary_key=True, max_length=20)
    StockName = models.CharField(null=True, blank=True, max_length=100)
    TradeVolume_Sell = models.FloatField(default=0)
    TradeVolume_Buy = models.FloatField(default=0)
    TradeVolume_NetBuy = models.FloatField(default=0)
    TradeAmount_Sell = models.FloatField(default=0)
    TradeAmount_Buy = models.FloatField(default=0)
    TradeAmount_NetBuy = models.FloatField(default=0)


class stockpriceinfo(models.Model):

    trade_date = models.CharField(null=False, blank=False, max_length=20)
    MarketType = models.CharField(null=False, blank=False, max_length=15)
    StockCode = models.CharField(null=False, blank=False, max_length=20)
    StockName = models.CharField(null=True, blank=True, max_length=100)
    OpenPrice = models.FloatField()
    HighPrice = models.FloatField()
    LowPrice = models.FloatField()
    ClosePrice = models.FloatField()
    TradeVolume = models.FloatField()
    StockPriceInfo_ID = models.CharField(null=False, blank=False, primary_key=True, max_length=150, default='')


class stockcalcdata(models.Model):

    trade_date = models.DateField(null=False, blank=False)
    StockCode = models.CharField(null=False, blank=False,  max_length=20)
    StockName = models.CharField(null=True, blank=True, max_length=100)
    MarketType = models.CharField(null=True, blank=True, max_length=15)
    ClosePrice = models.FloatField()
    TopBottomRate = models.FloatField()
    Ave20Volume = models.FloatField()
    Ave20VolWeight = models.FloatField()
    Ave12Price = models.FloatField()
    Ave26Price = models.FloatField()
    MaxHighPrice = models.FloatField()
    MinLowPrice = models.FloatField()
    SlowStoD = models.FloatField()
    STDevRate = models.FloatField()
    BolingerBandCenterBarr = models.FloatField()
    BolingerBandUpBarr = models.FloatField()
    BolingerBandDownBarr = models.FloatField()
    MACD = models.FloatField()
    Ave9MACDSignal = models.FloatField()
    MACDOsil = models.FloatField()
    MACDOsilRate = models.FloatField()
    RSI = models.FloatField()
    RSI_Flag = models.FloatField()
    OBV = models.FloatField()
    OBVSignal = models.FloatField()
    OBV_Flag = models.FloatField()
    VR = models.FloatField()
    VR_Flag = models.FloatField()
    StockCalcData_ID = models.CharField(null=False, blank=False, primary_key=True, max_length=150, default='')



class stockbarcodedata(models.Model):

    trade_date = models.DateField(null=False, blank=False)
    StockCode = models.CharField(null=False, blank=False, max_length=20)
    StockName = models.CharField(null=True, blank=True, max_length=100)
    MarketType = models.CharField(null=False, blank=False, max_length=15)
    ClosePrice = models.FloatField()
    BarType = models.CharField(null=True, blank=True, max_length=20)
    BarLengthType = models.CharField(null=True, blank=True, max_length=20)
    HammerType = models.CharField(null=True, blank=True, max_length=20)
    StochasticFlag = models.CharField(null=True, blank=True, max_length=20)
    BolingerBandPos = models.CharField(null=True, blank=True, max_length=20)
    VolumeFlag = models.CharField(null=True, blank=True, max_length=20)
    MACDFlag = models.CharField(null=True, blank=True, max_length=20)
    StrategyCond = models.CharField(null=True, blank=True, max_length=20)
    STDevStochasticFlag = models.CharField(null=True, blank=True, max_length=20)
    BarFinalCode = models.CharField(null=False, blank=False, max_length=20, default='')
    BarFinalCodeDtl = models.CharField(null=True, blank=True, max_length=20)
    StochasticCrossFlag = models.CharField(null=True, blank=True, max_length=20)

    StockBarcode_ID = models.CharField(null=False, blank=False, primary_key=True, max_length=150, default='')

    StockBarcodePerfReturn = models.ForeignKey(stockbarcodeperfreturn, on_delete=models.CASCADE, default='')
    StockBarcodePerfTotal = models.ForeignKey(stockbarcodeperftotal, on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    ListedStockInfo = models.ForeignKey(listedstockinfo, on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    StockPriceInfo = models.ForeignKey(stockpriceinfo, on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    StockCalcData = models.ForeignKey(stockcalcdata, on_delete=models.DO_NOTHING, db_constraint=False, null=True)

    AntBuySellInfo = models.ForeignKey(AntBuySellInfo, on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    ForeignBuySellInfo = models.ForeignKey(ForeignBuySellInfo, on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    InstituteBuySellInfo = models.ForeignKey(InstituteBuySellInfo, on_delete=models.DO_NOTHING, db_constraint=False, null=True)


class twinstockbarcodeperfreturn(models.Model):

    trade_date = models.DateField(null=False, blank=False)
    StockCode = models.CharField(null=False, blank=False,  max_length=20)
    StockName = models.CharField(null=True, blank=True, max_length=100)
    MarketType = models.CharField(null=False, blank=False, max_length=15)
    ClosePrice = models.FloatField()
    BarFinalCode = models.CharField(null=True, blank=True, max_length=20)
    BarFinalCodeDtl = models.CharField(null=True, blank=True, max_length=20)
    Day1PL = models.FloatField()
    Day1Return = models.FloatField()
    ClosePriceAft1 = models.FloatField()
    Day7PL = models.FloatField()
    Day7Return = models.FloatField()
    ClosePriceAft7 = models.FloatField()
    Day30PL = models.FloatField()
    Day30Return = models.FloatField()
    ClosePriceAft30 = models.FloatField()
    Day90PL = models.FloatField()
    Day90Return = models.FloatField()
    ClosePriceAft90 = models.FloatField()
    Day180PL = models.FloatField()
    Day180Return = models.FloatField()
    ClosePriceAft180 = models.FloatField()
    Day360PL = models.FloatField()
    Day360Return = models.FloatField()
    ClosePriceAft360 = models.FloatField()
    TodayPL = models.FloatField(null=True, blank=True)
    TodayReturn = models.FloatField(null=True, blank=True)

    StockBarcode_ID = models.CharField(null=False, blank=False, primary_key=True, max_length=150, default='')


class twinstockbarcodedata(models.Model):

    trade_date = models.DateField(null=False, blank=False)
    StockCode = models.CharField(null=False, blank=False, max_length=20)
    StockName = models.CharField(null=True, blank=True, max_length=100)
    MarketType = models.CharField(null=False, blank=False, max_length=15)
    ClosePrice = models.FloatField()
    BarType = models.CharField(null=True, blank=True, max_length=20)
    BarLengthType = models.CharField(null=True, blank=True, max_length=20)
    HammerType = models.CharField(null=True, blank=True, max_length=20)
    StochasticFlag = models.CharField(null=True, blank=True, max_length=20)
    BolingerBandPos = models.CharField(null=True, blank=True, max_length=20)
    VolumeFlag = models.CharField(null=True, blank=True, max_length=20)
    MACDFlag = models.CharField(null=True, blank=True, max_length=20)
    StrategyCond = models.CharField(null=True, blank=True, max_length=20)
    STDevStochasticFlag = models.CharField(null=True, blank=True, max_length=20)
    BarFinalCode = models.CharField(null=False, blank=False, max_length=20)
    BarFinalCodeDtl = models.CharField(null=True, blank=True, max_length=20)
    StochasticCrossFlag = models.CharField(null=True, blank=True, max_length=20)

    StockBarcode_ID = models.CharField(null=False, blank=False, primary_key=True, max_length=150, default='')

    TwinStockBarcodePerfReturn = models.ForeignKey(twinstockbarcodeperfreturn, on_delete=models.CASCADE, default='')
    StockBarcodePerfTotal = models.ForeignKey(stockbarcodeperftotal, on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    ListedStockInfo = models.ForeignKey(listedstockinfo, on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    StockPriceInfo = models.ForeignKey(stockpriceinfo, on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    StockCalcData = models.ForeignKey(stockcalcdata, on_delete=models.DO_NOTHING, db_constraint=False, null=True)

    AntBuySellInfo = models.ForeignKey(AntBuySellInfo, on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    ForeignBuySellInfo = models.ForeignKey(ForeignBuySellInfo, on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    InstituteBuySellInfo = models.ForeignKey(InstituteBuySellInfo, on_delete=models.DO_NOTHING, db_constraint=False, null=True)

