import django_filters
from .models import Ticket, Category
from django.utils.translation import gettext_lazy as _

class TicketFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=Ticket.STATUS_CHOICES,
        label=_("Статус"),
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label=_("Категория"),
    )

    class Meta:
        model = Ticket
        fields = ['status', 'category']