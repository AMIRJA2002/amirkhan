# Generated by Django 5.1.1 on 2024-10-15 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_userchatid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userchatid',
            name='chat_id',
            field=models.CharField(default=None, max_length=10000),
            preserve_default=False,
        ),
    ]
