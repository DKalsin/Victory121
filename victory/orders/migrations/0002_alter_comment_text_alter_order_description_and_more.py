# Generated by Django 4.0.1 on 2022-01-12 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='order',
            name='description',
            field=models.TextField(max_length=1000, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='order',
            name='title',
            field=models.CharField(max_length=500, verbose_name='title'),
        ),
    ]
