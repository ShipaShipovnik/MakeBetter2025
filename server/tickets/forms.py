from django import forms
from .models import Ticket, TicketAttachment, Category


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


class TicketCommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Причина отклонения, комментарий.',
            'class': 'form-control descrpt',
        }),
        label='Комментарий',
        required=True,
    )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'catg-form catg-add-form',
                'placeholder': 'Название категории'
            }),
        }
