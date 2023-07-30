from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User


def index(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        if email:
            try:
                existing_user = User.objects.get(username=email)
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    return render(request, 'index.html', {'user': request.user})
                else:
                    error_message = "Неверный пароль"
                    messages.error(request, error_message)
            except User.DoesNotExist:
                new_user = User.objects.create_user(username=email, email=email, password=password)
                login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                new_user.save()
        else:
            error_message = "Введите почту"
            messages.error(request, error_message)

    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def tests(requests):
    print('ВСЕ ТЕСТЫ')


def add_test(requests):
    print('ДОБАВЛЕНИЕ')