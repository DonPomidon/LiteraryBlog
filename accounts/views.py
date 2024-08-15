from .forms import RegisterCustomUser, LoginCustomUser
from django.contrib.auth import login, logout as auth_logout
from django.shortcuts import render, redirect


def login_user(request):
    if request.method == 'POST':
        form = LoginCustomUser(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('blog:book_list')
            else:
                return render(request, 'blog/books/login.html', {'form': form})
    else:
        form = LoginCustomUser()
        return render(request, 'blog/books/login.html', {'form': form})


def register_user(request):
    if request.method == 'POST':
        form = RegisterCustomUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        else:
            form.add_error(None, 'Wrong data, try again!')
    else:
        form = RegisterCustomUser

    return render(request, 'blog/books/register.html', {'form': form})


def logout_user(request):
    auth_logout(request)
    return redirect('blog:book_list')
