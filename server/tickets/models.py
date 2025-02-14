from django.db import models
from users.models import User
from django.utils import timezone


# Категория =======================================================
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Новая'),
        ('SOLVED', 'Решена'),
        ('DECLINED', 'Отклонена'),
    ]
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='NEW')

    title = models.CharField(max_length=300)
    description = models.TextField(max_length=350)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    created_by = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    solved_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата решения')

    def __str__(self):
        return f" {self.get_status_display()} - {self.title}"

    class Meta:
        verbose_name_plural = "Заявки"
        verbose_name = "Заявки"

    def save(self, *args, **kwargs):
        # Если статус изменён на "Решено" и раньше был другим
        if self.status == 'SOLVED' and self.pk:
            old_status = Ticket.objects.get(pk=self.pk).status
            if old_status != 'SOLVED':
                self.solved_at = timezone.now()  # Устанавливаем текущую дату и время
        # Если статус "Решено" и это новый объект
        elif self.status == 'SOLVED' and not self.pk:
            self.solved_at = timezone.now()

        super().save(*args, **kwargs)


class TicketAttachment(models.Model):
    TYPE_CHOICES = [
        ('BEFORE', 'Фото "до"'),
        ('AFTER', 'Фото "после"'),
    ]

    ticket = models.ForeignKey(Ticket, related_name='attachments', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='tickets/attachments/', verbose_name='Фото')
    type = models.CharField(max_length=6, choices=TYPE_CHOICES, verbose_name='Тип фото')

    def __str__(self):
        return f"{self.get_type_display()} для заявки #{self.ticket.title}"

    class Meta:
        verbose_name_plural = "Фото заявок"
        verbose_name = "Фото заявки"
