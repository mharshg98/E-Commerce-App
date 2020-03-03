# Generated by Django 2.2.6 on 2019-12-21 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20191218_2333'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=5000)),
                ('phone', models.CharField(default='', max_length=50)),
                ('email', models.CharField(default='', max_length=50)),
            ],
        ),
    ]
