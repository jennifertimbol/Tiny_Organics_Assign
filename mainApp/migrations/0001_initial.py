# Generated by Django 2.2 on 2021-07-21 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=55)),
                ('last_name', models.CharField(max_length=55)),
                ('email', models.CharField(max_length=75)),
                ('password', models.CharField(max_length=55)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=55)),
                ('last_name', models.CharField(max_length=55)),
                ('allergies', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Customer')),
            ],
        ),
    ]