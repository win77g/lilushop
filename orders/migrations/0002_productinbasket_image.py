# Generated by Django 2.2.4 on 2019-08-17 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinbasket',
            name='image',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
    ]
