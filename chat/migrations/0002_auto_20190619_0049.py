# Generated by Django 2.0.4 on 2019-06-18 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='created',
            field=models.DateTimeField(),
        ),
    ]