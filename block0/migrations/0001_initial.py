# Generated by Django 3.1.5 on 2021-05-03 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlockDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block', models.TextField(max_length=20)),
                ('nonce', models.IntegerField()),
                ('merkleroot', models.TextField(max_length=64)),
                ('previous_hash', models.TextField(max_length=64)),
                ('finalhash', models.TextField(max_length=64)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_pub', models.TextField()),
                ('s_pub', models.TextField()),
                ('amount', models.IntegerField()),
                ('previous_hash', models.TextField()),
                ('current_hash', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
