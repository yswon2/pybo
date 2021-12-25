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




class StockBarcodeData(models.Model):

    trade_date = models.DateField(null=False, blank=False)
    StockCode = models.CharField(null=False, blank=False, max_length=45)
    StockName = models.CharField(null=True, blank=True, max_length=100)
    MarketType = models.CharField(null=False, blank=False, max_length=45)
    ClosePrice = models.FloatField()
    BarType = models.CharField(null=True, blank=True, max_length=45)
    BarLengthType = models.CharField(null=True, blank=True, max_length=45)
    HammerType = models.CharField(null=True, blank=True, max_length=45)
    StochasticFlag = models.CharField(null=True, blank=True, max_length=45)
    BolingerBandPos = models.CharField(null=True, blank=True, max_length=45)
    VolumeFlag = models.CharField(null=True, blank=True, max_length=45)
    MACDFlag = models.CharField(null=True, blank=True, max_length=45)
    StrategyCond = models.CharField(null=True, blank=True, max_length=45)
    STDevStochasticFlag = models.CharField(null=True, blank=True, max_length=45)
    BarFinalCode = models.CharField(null=True, blank=True, max_length=45)
    BarFinalCodeDtl = models.CharField(null=True, blank=True, max_length=45)
    StochasticCrossFlag = models.CharField(null=True, blank=True, max_length=45)

    #StockBarcode_ID = '_'.join(trade_date.strftime('%Y-%m-%d'), StockCode, MarketType)
    StockBarcode_ID = models.CharField(null=False, blank=False, primary_key=True, max_length=150, default='AAA')

class StockBarcodePerfReturn(models.Model):

    #TradeDate = models.DateField(null=False, blank=False)
    #StockCode = models.CharField(null=False, blank=False,  max_length=45)
    #StockName = models.CharField(null=True, blank=True, max_length=100)
    #MarketType = models.CharField(null=True, blank=True, max_length=45)
    #ClosePrice = models.FloatField()
    #BarFinalCode = models.CharField(null=True, blank=True, max_length=45)
    #BarFinalCodeDtl = models.CharField(null=True, blank=True, max_length=45)
    Day1PL = models.FloatField()
    Day1Return = models.FloatField()
    ClosePriceAft1 = models.FloatField()
    Day5PL = models.FloatField()
    Day5Return = models.FloatField()
    ClosePriceAft5 = models.FloatField()
    Day25PL = models.FloatField()
    Day25Return = models.FloatField()
    ClosePriceAft25 = models.FloatField()
    Day75PL = models.FloatField()
    Day75Return = models.FloatField()
    ClosePriceAft75 = models.FloatField()

    StockBarcodeData = models.ForeignKey(StockBarcodeData, on_delete=models.CASCADE, default='AAA')


class StockBarcodePerfTotal(models.Model):

    #StockBarcodePerfTotal_ID = '_'.join(BarFinalCode, MarketType)
    StockBarcodePerfTotal_ID = models.CharField(null=False, blank=False, primary_key=True, max_length=150, default='AAA')
    BarFinalCode = models.CharField(null=False, blank=False, max_length=45)
    MarketType = models.CharField(null=False, blank=False,  max_length=45)
    #StockBarcodeData = models.ForeignKey(StockBarcodeData, on_delete=models.CASCADE)
    TotDay1Return = models.FloatField()
    TotDay5Return = models.FloatField()
    TotDay25Return = models.FloatField()
    TotDay75Return = models.FloatField()
    BarFinalCode_Cnt = models.IntegerField()
    TotDay1Average = models.FloatField()
    TotDay5Average = models.FloatField()
    TotDay25Average = models.FloatField()
    TotDay75Average = models.FloatField()
    PlusTotDay1Return = models.FloatField()
    MinusTotDay1Return = models.FloatField()
    PlusTotDay5Return = models.FloatField()
    MinusTotDay5Return = models.FloatField()
    PlusTotDay25Return = models.FloatField()
    MinusTotDay25Return = models.FloatField()
    PlusTotDay75Return = models.FloatField()
    MinusTotDay75Return = models.FloatField()
    PlusDay1BarCode_Cnt = models.IntegerField()
    MinusDay1BarCode_Cnt = models.IntegerField()
    PlusDay5BarCode_Cnt = models.IntegerField()
    MinusDay5BarCode_Cnt = models.IntegerField()
    PlusDay25BarCode_Cnt = models.IntegerField()
    MinusDay25BarCode_Cnt = models.IntegerField()
    PlusDay75BarCode_Cnt = models.IntegerField()
    MinusDay75BarCode_Cnt = models.IntegerField()
    PlusTotDay1Average = models.FloatField()
    MinusTotDay1Average = models.FloatField()
    PlusTotDay5Average = models.FloatField()
    MinusTotDay5Average = models.FloatField()
    PlusTotDay25Average = models.FloatField()
    MinusTotDay25Average = models.FloatField()
    PlusTotDay75Average = models.FloatField()
    MinusTotDay75Average = models.FloatField()
    TotDay5MaxReturn = models.FloatField()
    TotDay25MaxReturn = models.FloatField()
    TotDay75MaxReturn = models.FloatField()
    TotDay5MinReturn = models.FloatField()
    TotDay25MinReturn = models.FloatField()
    TotDay75MinReturn = models.FloatField()
    Day5SuccessRate = models.FloatField()
    Day25SuccessRate = models.FloatField()
    #BarFinalCodeDtl = models.CharField(null=True, blank=True, max_length=45)
    Day1SuccessRate = models.FloatField()
