from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TicketForm, TicketAttachmentForm


def home(request):
    return render(request, 'main-page.html')


@login_required
def create_ticket(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        attachment_form = TicketAttachmentForm(request.POST, request.FILES)

        if ticket_form.is_valid() and attachment_form.is_valid():
            # Сохраняем тикет
            ticket = ticket_form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()

            # Сохраняем вложение с типом "ДО"
            attachment = attachment_form.save(commit=False)
            attachment.ticket = ticket
            attachment.type = 'BEFORE'
            attachment.save()

            return redirect('profile')
    else:
        ticket_form = TicketForm()
        attachment_form = TicketAttachmentForm()

    context = {
        'ticket_form': ticket_form,
        'attachment_form': attachment_form,
    }
    return render(request, 'create_ticket.html', context)
