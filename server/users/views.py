from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from tickets.models import Category, Ticket

from tickets.forms import CategoryForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.name = form.cleaned_data['name']
            user.save()
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        print('Вы успешно вышли')
        return redirect('home')
    return render(request, 'logout.html')


@login_required
def profile_view(request):
    user = request.user
    tickets = Ticket.objects.filter(created_by=user)
    categories = Category.objects.all()

    catg_form = CategoryForm(request.POST)

    context = {
        'user': user,
        'tickets': tickets,
        'categories': categories,
        'catg_form': catg_form,
    }
    return render(request, 'profile.html', context)