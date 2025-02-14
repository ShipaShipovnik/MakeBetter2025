from django.contrib import admin
from .models import *

from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке
    list_display = ('title', 'status', 'created_at', 'solved_at', 'created_by', 'category')

    # Поля на странице редактирования
    fields = ('title', 'description', 'status', 'solved_at', 'category', 'created_by')

    # Поля только для чтения
    readonly_fields = ('solved_at',)

    # Фильтры
    list_filter = ('status',)

    # Поиск
    search_fields = ('title', 'description')

admin.site.register(Category)
admin.site.register(TicketAttachment)
