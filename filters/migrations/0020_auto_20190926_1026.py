# Generated by Django 2.2.4 on 2019-09-26 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0019_auto_20190925_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filterselect',
            name='filter_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filters.FilterCategory', to_field='name', verbose_name='Filter Category'),
        ),
    ]
