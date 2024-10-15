from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'خوش آمدید')
            return redirect('home:home')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')

    return render(request, 'login.html')


def user_signup(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        User = get_user_model()

        if User.objects.filter(phone_number=phone).exists():
            messages.error(request, 'این شماره موبایل قبلاً ثبت شده است.')
        else:
            user = User.objects.create(
                phone_number=phone,
                full_name=last_name,
                password=make_password(password)
            )
            messages.success(request, 'ثبت نام با موفقیت انجام شد. لطفاً وارد شوید.')
            login(request, user)
            return redirect('home:home')

    return render(request, 'register.html')