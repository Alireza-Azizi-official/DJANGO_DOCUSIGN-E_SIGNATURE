# Generated by Django 5.1.4 on 2024-12-18 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0005_alter_contract_contract_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='contract_text',
            field=models.TextField(default='It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. \n                                                The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using Content here, content here, \n                                                making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, \n                                                and a search for lorem ipsum will uncover many web sites still in their infancy. Various versions have evolved over the years, \n                                                sometimes by accident, sometimes on purpose. Please sign the contract here: ~signature~'),
        ),
    ]
