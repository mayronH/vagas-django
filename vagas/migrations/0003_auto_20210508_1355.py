# Generated by Django 3.2 on 2021-05-08 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vagas', '0002_auto_20210508_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidacy',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='candidatos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='candidacy',
            name='opportunity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vagas', to='vagas.opportunity'),
        ),
        migrations.AlterField(
            model_name='candidacy',
            name='schooling',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='escolaridades', to='vagas.schooling'),
        ),
    ]
