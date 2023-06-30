# Generated by Django 4.0.7 on 2023-06-30 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('copias_id', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('prazo', models.DateTimeField()),
                ('devolvido', models.BooleanField(default=False)),
            ],
        ),
    ]
