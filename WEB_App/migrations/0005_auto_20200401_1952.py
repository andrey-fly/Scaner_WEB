# Generated by Django 3.0.3 on 2020-04-01 16:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('WEB_App', '0004_remove_comment_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userphoto',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Создано'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userphoto',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AlterField(
            model_name='goodsonmoderation',
            name='status',
            field=models.CharField(choices=[(1, 'Принято на модерацию'), (2, 'Одобрено'), (3, 'Отклонено')], default='Принято на модерацию', max_length=25, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='userphoto',
            name='img',
            field=models.ImageField(default='profile_icon', null=True, upload_to='photos'),
        ),
    ]
