from django.shortcuts import render, redirect, get_object_or_404
from .models import Tasks, Categories, Subtasks
from .forms import TasksForm, CategoriesForm, SubtasksForm
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Count, Case, When, Value, FloatField

""""TASKS"""

@login_required
def tasks_list(request):
    tasks = Tasks.objects.prefetch_related('category', 'subtasks').filter(user=request.user)
    tasks = tasks.annotate(
        total=Count('subtasks'),
        completed=Count('subtasks', filter=Q(subtasks__is_active=False)),
        percent=Case(
            When(total=0, then=Value(0.0)),
            default=(F('completed') * 100.0 / F('total')),
            output_field=FloatField()
        )
    )
    status = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort_by')


    if sort_by == 'priority':
        tasks = tasks.order_by('priority')
    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    if status == 'completed':
        tasks = tasks.filter(is_active=False)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if category_filter:
        tasks = tasks.filter(category__id=category_filter)
    
    context = {
        'tasks': tasks,
        'categories': Categories.objects.filter(user=request.user),
        'subform': SubtasksForm()
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


""""CATEGORIES"""

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

"""SubTasks"""
@login_required
def subtask_create(request, task_pk):
    parent_task = get_object_or_404(Tasks, pk=task_pk, user=request.user)
    if request.method == 'POST':
        form = SubtasksForm(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.task = parent_task
            subtask.save()
    return redirect('tasks_list')
        
        

@login_required
def subtask_toggle(request, pk):
    if request.method == 'POST':
        subtask = get_object_or_404(Subtasks, pk=pk, task__user=request.user)
        subtask.is_active = not subtask.is_active
        subtask.save()
        return redirect('tasks_list')
