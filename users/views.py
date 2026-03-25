from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def home(request):
    if request.user.is_authenticated:
        return redirect('tasks_list')
    return render(request, 'users/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks_list')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)