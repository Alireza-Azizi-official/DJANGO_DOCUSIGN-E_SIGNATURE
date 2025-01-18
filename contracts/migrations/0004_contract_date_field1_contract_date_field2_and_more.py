# Generated by Django 5.1.4 on 2024-12-18 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0003_alter_contract_contract_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='date_field1',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='date_field2',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='name_field',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='signed_at_recipient',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='signed_at_user',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
