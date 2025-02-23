from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone

from .forms import TicketForm, TicketAttachmentForm, CategoryForm, TicketCommentForm
from .models import Category, Ticket, TicketComment


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
    return render(request, 'create-ticket.html', context)


def create_category(request):
    if request.method == 'POST':
        catg_form = CategoryForm(request.POST)
        catg = catg_form.save(commit=False)
        catg.save()

        return redirect('profile')
    else:
        ticket_form = TicketForm()


def delete_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        try:
            catg = Category.objects.get(pk=category_id)
            catg.delete()
            messages.success(request, 'Категория успешно удалена.')
        except Category.DoesNotExist:
            messages.error(request, 'Категория не найдена.')
        return redirect('profile')
    else:
        return redirect('profile')


def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff)
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    attachment_form = TicketAttachmentForm(request.POST or None, request.FILES or None)
    comment_form = TicketCommentForm(request.POST or None)

    if request.method == 'POST':
        # Обработка решения заявки
        if 'solve_ticket' in request.POST:
            if attachment_form.is_valid():
                # Сохраняем фото "после"
                attachment = attachment_form.save(commit=False)
                attachment.ticket = ticket
                attachment.type = 'AFTER'
                attachment.save()

                # Обновляем статус тикета
                ticket.status = 'SOLVED'
                ticket.solved_at = timezone.now()
                ticket.save()

                messages.success(request, 'Заявка решена и фото добавлено')
                return redirect('ticket_detail', ticket_id=ticket.id)

        # Обработка отклонения заявки
        elif 'decline_ticket' in request.POST:
            if comment_form.is_valid():
                # Создаем комментарий
                TicketComment.objects.create(
                    ticket=ticket,
                    user=request.user,
                    comment=comment_form.cleaned_data['comment']
                )

                # Обновляем статус тикета
                ticket.status = 'DECLINED'
                ticket.save()

                messages.success(request, 'Заявка отклонена')
                return redirect('ticket_detail', ticket_id=ticket.id)

    # Получаем все вложения для отображения
    before_images = ticket.attachments.filter(type='BEFORE')
    after_images = ticket.attachments.filter(type='AFTER')

    return render(request, 'ticket-detail.html', {
        'ticket': ticket,
        'solve_form': attachment_form,
        'decline_form': comment_form,
        'before_images': before_images,
        'after_images': after_images,
    })
