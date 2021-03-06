# Generated by Django 2.2.4 on 2019-09-28 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0025_auto_20190928_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filterselect',
            name='name',
            field=models.CharField(blank=True, max_length=250, unique=True),
        ),
        migrations.RemoveField(
            model_name='productfilter',
            name='values',
        ),
        migrations.AddField(
            model_name='productfilter',
            name='values',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filtervalues', to='filters.FilterSelect', to_field='name', verbose_name='Values'),
        ),
    ]
