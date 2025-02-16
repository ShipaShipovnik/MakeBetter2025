from django import forms
from .models import Ticket, TicketAttachment


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control title',
                'placeholder': 'Заголовок'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control descrpt',
                'placeholder': 'Кратко опишите проблему'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'  # Ваши классы
            }),
        }


class TicketAttachmentForm(forms.ModelForm):
    class Meta:
        model = TicketAttachment
        fields = ['photo']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
