from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        return render(request, 'signin.html', context={'error': 'Invalid username or password'})
    return render(request, 'signin.html')


@login_required(login_url='/auth/login')
def logout_view(request):
    logout(request)
    return redirect('auth/login')



