# Generated by Django 5.0 on 2024-02-27 14:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FutsalOwner',
            fields=[
                ('owner_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('address', models.TextField(max_length=100)),
                ('password', models.CharField(max_length=50)),
                ('otp', models.CharField(default='0000', max_length=25)),
                ('status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]