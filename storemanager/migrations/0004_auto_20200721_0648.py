# Generated by Django 2.2.14 on 2020-07-21 03:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storemanager', '0003_auto_20200721_0620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='export_to_csv',
        ),
        migrations.AlterField(
            model_name='stock',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='storemanager.Category'),
        ),
    ]