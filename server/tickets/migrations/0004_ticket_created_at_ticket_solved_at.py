# Generated by Django 5.1.3 on 2025-02-14 23:14

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0003_alter_ticket_options_ticketattachment"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ticket",
            name="solved_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Дата решения"
            ),
        ),
    ]
