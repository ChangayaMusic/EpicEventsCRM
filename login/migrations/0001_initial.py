# Generated by Django 5.0.2 on 2024-02-20 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('department', models.CharField(choices=[('Sales', 'Sales'), ('Support', 'Support'), ('Management', 'Management')], max_length=100)),
                ('hashed_password', models.CharField(max_length=128)),
            ],
        ),
    ]
