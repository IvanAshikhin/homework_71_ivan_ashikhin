# Generated by Django 4.1.7 on 2023-04-19 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/Default.jpg', null=True, upload_to='avatars', verbose_name='Аватар'),
        ),
    ]