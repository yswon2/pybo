# Generated by Django 3.1.3 on 2022-01-04 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField()),
                ('modify_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_answer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='stockbarcodeperfreturn',
            fields=[
                ('trade_date', models.DateField()),
                ('StockCode', models.CharField(max_length=20)),
                ('StockName', models.CharField(blank=True, max_length=100, null=True)),
                ('MarketType', models.CharField(max_length=15)),
                ('ClosePrice', models.FloatField()),
                ('BarFinalCode', models.CharField(blank=True, max_length=20, null=True)),
                ('BarFinalCodeDtl', models.CharField(blank=True, max_length=20, null=True)),
                ('Day1PL', models.FloatField()),
                ('Day1Return', models.FloatField()),
                ('ClosePriceAft1', models.FloatField()),
                ('Day7PL', models.FloatField()),
                ('Day7Return', models.FloatField()),
                ('ClosePriceAft7', models.FloatField()),
                ('Day30PL', models.FloatField()),
                ('Day30Return', models.FloatField()),
                ('ClosePriceAft30', models.FloatField()),
                ('Day90PL', models.FloatField()),
                ('Day90Return', models.FloatField()),
                ('ClosePriceAft90', models.FloatField()),
                ('Day180PL', models.FloatField()),
                ('Day180Return', models.FloatField()),
                ('ClosePriceAft180', models.FloatField()),
                ('Day360PL', models.FloatField()),
                ('Day360Return', models.FloatField()),
                ('ClosePriceAft360', models.FloatField()),
                ('StockBarcode_ID', models.CharField(default='', max_length=150, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='stockbarcodeperftotal',
            fields=[
                ('BarFinalCode', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('MarketType', models.CharField(max_length=15)),
                ('TotDay1Return', models.FloatField()),
                ('TotDay7Return', models.FloatField()),
                ('TotDay30Return', models.FloatField()),
                ('TotDay90Return', models.FloatField()),
                ('TotDay180Return', models.FloatField()),
                ('TotDay360Return', models.FloatField()),
                ('BarFinalCode_Cnt', models.IntegerField()),
                ('TotDay1Average', models.FloatField()),
                ('TotDay7Average', models.FloatField()),
                ('TotDay30Average', models.FloatField()),
                ('TotDay90Average', models.FloatField()),
                ('TotDay180Average', models.FloatField()),
                ('TotDay360Average', models.FloatField()),
                ('PlusTotDay1Return', models.FloatField()),
                ('MinusTotDay1Return', models.FloatField()),
                ('PlusTotDay7Return', models.FloatField()),
                ('MinusTotDay7Return', models.FloatField()),
                ('PlusTotDay30Return', models.FloatField()),
                ('MinusTotDay30Return', models.FloatField()),
                ('PlusTotDay90Return', models.FloatField()),
                ('MinusTotDay90Return', models.FloatField()),
                ('PlusTotDay180Return', models.FloatField()),
                ('MinusTotDay180Return', models.FloatField()),
                ('PlusTotDay360Return', models.FloatField()),
                ('MinusTotDay360Return', models.FloatField()),
                ('PlusDay1BarCode_Cnt', models.IntegerField()),
                ('MinusDay1BarCode_Cnt', models.IntegerField()),
                ('PlusDay7BarCode_Cnt', models.IntegerField()),
                ('MinusDay7BarCode_Cnt', models.IntegerField()),
                ('PlusDay30BarCode_Cnt', models.IntegerField()),
                ('MinusDay30BarCode_Cnt', models.IntegerField()),
                ('PlusDay90BarCode_Cnt', models.IntegerField()),
                ('MinusDay90BarCode_Cnt', models.IntegerField()),
                ('PlusDay180BarCode_Cnt', models.IntegerField()),
                ('MinusDay180BarCode_Cnt', models.IntegerField()),
                ('PlusDay360BarCode_Cnt', models.IntegerField()),
                ('MinusDay360BarCode_Cnt', models.IntegerField()),
                ('PlusTotDay1Average', models.FloatField()),
                ('MinusTotDay1Average', models.FloatField()),
                ('PlusTotDay7Average', models.FloatField()),
                ('MinusTotDay7Average', models.FloatField()),
                ('PlusTotDay30Average', models.FloatField()),
                ('MinusTotDay30Average', models.FloatField()),
                ('PlusTotDay90Average', models.FloatField()),
                ('MinusTotDay90Average', models.FloatField()),
                ('PlusTotDay180Average', models.FloatField()),
                ('MinusTotDay180Average', models.FloatField()),
                ('PlusTotDay360Average', models.FloatField()),
                ('MinusTotDay360Average', models.FloatField()),
                ('TotDay7MaxReturn', models.FloatField()),
                ('TotDay30MaxReturn', models.FloatField()),
                ('TotDay90MaxReturn', models.FloatField()),
                ('TotDay180MaxReturn', models.FloatField()),
                ('TotDay360MaxReturn', models.FloatField()),
                ('TotDay7MinReturn', models.FloatField()),
                ('TotDay30MinReturn', models.FloatField()),
                ('TotDay90MinReturn', models.FloatField()),
                ('TotDay180MinReturn', models.FloatField()),
                ('TotDay360MinReturn', models.FloatField()),
                ('Day7SuccessRate', models.FloatField()),
                ('Day30SuccessRate', models.FloatField()),
                ('Day1SuccessRate', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='stockbarcodedata',
            fields=[
                ('trade_date', models.DateField()),
                ('StockCode', models.CharField(max_length=20)),
                ('StockName', models.CharField(blank=True, max_length=100, null=True)),
                ('MarketType', models.CharField(max_length=15)),
                ('ClosePrice', models.FloatField()),
                ('BarType', models.CharField(blank=True, max_length=20, null=True)),
                ('BarLengthType', models.CharField(blank=True, max_length=20, null=True)),
                ('HammerType', models.CharField(blank=True, max_length=20, null=True)),
                ('StochasticFlag', models.CharField(blank=True, max_length=20, null=True)),
                ('BolingerBandPos', models.CharField(blank=True, max_length=20, null=True)),
                ('VolumeFlag', models.CharField(blank=True, max_length=20, null=True)),
                ('MACDFlag', models.CharField(blank=True, max_length=20, null=True)),
                ('StrategyCond', models.CharField(blank=True, max_length=20, null=True)),
                ('STDevStochasticFlag', models.CharField(blank=True, max_length=20, null=True)),
                ('BarFinalCode', models.CharField(default='', max_length=20)),
                ('BarFinalCodeDtl', models.CharField(blank=True, max_length=20, null=True)),
                ('StochasticCrossFlag', models.CharField(blank=True, max_length=20, null=True)),
                ('StockBarcode_ID', models.CharField(default='', max_length=150, primary_key=True, serialize=False)),
                ('StockBarcodePerfReturn', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='pybo.stockbarcodeperfreturn')),
                ('StockBarcodePerfTotal', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pybo.stockbarcodeperftotal')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField()),
                ('modify_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_question', to=settings.AUTH_USER_MODEL)),
                ('voter', models.ManyToManyField(related_name='voter_question', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField()),
                ('modify_date', models.DateTimeField(blank=True, null=True)),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pybo.answer')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pybo.question')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pybo.question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='voter',
            field=models.ManyToManyField(related_name='voter_answer', to=settings.AUTH_USER_MODEL),
        ),
    ]
