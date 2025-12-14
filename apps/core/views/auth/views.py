from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from ...forms import UserRegistrationForm

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Qeydiyyat uğurla tamamlandı! Profiliniz yaradıldı.')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Xoş gəldiniz, {user.get_full_name()}!')
            return redirect('profile')
        else:
            messages.error(request, 'İstifadəçi adı və ya şifrə yanlışdır.')
    
    return render(request, 'auth/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Uğurla çıxış etdiniz.')
    return redirect('home')