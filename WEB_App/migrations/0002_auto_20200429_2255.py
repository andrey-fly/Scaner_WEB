# Generated by Django 3.0.3 on 2020-04-29 19:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('WEB_App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='checked',
            field=models.BooleanField(default=False, verbose_name='Проверено ли'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата отправки'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ComplaintResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата отправки ответа')),
                ('text', models.TextField(verbose_name='Содержимое ответа на жалобу')),
                ('checked', models.BooleanField(default=False, verbose_name='Прочитано ли')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WEB_App.Complaint', verbose_name='Жалоба')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]