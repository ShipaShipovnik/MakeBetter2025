import os

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
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

        # Проверка, что при статусе "ОТКЛОНЕНО" есть комментарий
        if self.status == 'DECLINED' and self.pk:
            if not self.comments.exists():  # Проверяем, есть ли комментарии
                raise ValidationError("При отклонении заявки необходимо добавить комментарий.")

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Удаляем все связанные файлы
        for attachment in self.attachments.all():
            if attachment.photo:
                file_path = attachment.photo.path
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Ошибка при удалении файла {file_path}: {e}")
        # Удаляем все записи TicketAttachment
        self.attachments.all().delete()
        # Вызываем стандартный метод delete
        super().delete(*args, **kwargs)


class TicketAttachment(models.Model):
    TYPE_CHOICES = [
        ('BEFORE', 'Фото "до"'),
        ('AFTER', 'Фото "после"'),
    ]

    ticket = models.ForeignKey(Ticket, related_name='attachments', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='tickets/attachments/', verbose_name='Фото')
    type = models.CharField(max_length=6, choices=TYPE_CHOICES, verbose_name='Тип фото', default='BEFORE')

    def __str__(self):
        return f"{self.get_type_display()} для заявки #{self.ticket.title}"

    class Meta:
        verbose_name_plural = "Фото заявок"
        verbose_name = "Фото заявки"


class TicketComment(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_comments')
    comment = models.TextField(max_length=500, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.user.name} к тикету #{self.ticket.id}"

    class Meta:
        verbose_name = 'Комментарий к заявке'
        verbose_name_plural = 'Комментарии к заявкам'
