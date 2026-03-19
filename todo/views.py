from django.shortcuts import render, redirect, get_object_or_404
from .models import Tasks, Categories
from .forms import TasksForm, CategoriesForm
from django.contrib.auth.decorators import login_required


@login_required
def tasks_list(request):
    tasks = Tasks.objects.prefetch_related('category').filter(user=request.user)
    context = {
        'tasks': tasks,
    }
    return render(request, 'todo/tasks_list.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TasksForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            form.save_m2m()
            return redirect('tasks_list')
    else:
        form = TasksForm()
    context = {
        'form': form,
    }
    return render(request, 'todo/task_form.html', context)


@login_required
def task_toggle(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Tasks, pk=pk, user=request.user)
        task.is_active = not task.is_active
        task.save()
    return redirect('tasks_list')

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Tasks, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('tasks_list')


@login_required
def category_list(request):
    category = Categories.objects.filter(user=request.user)
    context = {
        'categories': category
    }
    return render(request, 'todo/category_list.html', context)

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoriesForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category_list')
    else:
        form = CategoriesForm()
    context = {
        'form': form,
    }
    return render(request, 'todo/category_form.html', context)

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Categories, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
    return redirect('category_list')