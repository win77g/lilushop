# Generated by Django 2.2.4 on 2019-09-22 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_auto_20190922_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='deep',
            name='category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='attributs',
            name='deep',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Deep', verbose_name='Глубина'),
        ),
    ]
