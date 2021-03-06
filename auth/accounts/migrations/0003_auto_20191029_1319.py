# Generated by Django 2.2.6 on 2019-10-29 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_phoneotp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phoneotp',
            name='forgot',
        ),
        migrations.RemoveField(
            model_name='phoneotp',
            name='forgot_logged',
        ),
        migrations.RemoveField(
            model_name='phoneotp',
            name='logged',
        ),
        migrations.AddField(
            model_name='phoneotp',
            name='validated',
            field=models.BooleanField(default=False, help_text='True if OTP is verified'),
        ),
    ]
