# Generated by Django 5.0 on 2024-02-18 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_alter_consumer_address_alter_consumer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumer',
            name='otp',
            field=models.CharField(default='0000', max_length=25),
        ),
        migrations.AddField(
            model_name='consumer',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]