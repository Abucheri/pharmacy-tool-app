# Generated by Django 2.2.14 on 2020-07-21 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storemanager', '0002_auto_20200721_0558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='storemanager.Category'),
            preserve_default=False,
        ),
    ]
