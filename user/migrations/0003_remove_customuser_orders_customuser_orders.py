# Generated by Django 4.1.3 on 2022-11-11 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
        ('user', '0002_customuser_cart_customuser_orders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='orders',
        ),
        migrations.AddField(
            model_name='customuser',
            name='orders',
            field=models.ManyToManyField(related_name='user_orders', to='app.order'),
        ),
    ]
