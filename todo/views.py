from django.shortcuts import render, redirect, get_object_or_404
from .models import Tasks, Categories, Subtasks
from .forms import TasksForm, CategoriesForm, SubtasksForm
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Count, Case, When, Value, FloatField
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone


""""TASKS"""

class TaskListView(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'todo/tasks_list.html'   # Ссылка на штмльку
    context_object_name = 'page' #имя контекста как было в FBV (такое имя ибо делали пагинацию)
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        qs = qs.prefetch_related('category', 'subtasks')
        
        '''ANNOTATIONS'''
        qs = qs.annotate(
            total=Count('subtasks'),
            completed=Count('subtasks', filter=Q(subtasks__is_active=False)),
            percent=Case(
                When(total=0, then=Value(0.0)),
                default=(F('completed')* 100.0 / F('total')),
                output_field=FloatField()
            )
        )

        '''GET PARAMS'''
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        category_id = self.request.GET.get('category')
        search_query = self.request.GET.get('search')
        sort_by = self.request.GET.get('sort_by')

        """FILTER"""
        if status == 'completed':
            qs = qs.filter(is_active=False)
        if priority:
            qs = qs.filter(priority=priority)
        if category_id:
            qs = qs.filter(category__id=category_id)
        if search_query:
            qs = qs.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

        """SORTING"""
        sort_fields = {
            'priority_desc': '-priority',
            'priority_asc': 'priority',
            'created_desc': '-created_at',
            'created_asc': 'created_at',
        }
        if sort_by in sort_fields:
            qs = qs.order_by(sort_fields[sort_by])
        else:
            qs = qs.order_by('-created_at')
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Categories.objects.filter(user=self.request.user)
        context['subform'] = SubtasksForm()
        get_params = {
            'status': self.request.GET.get('status'),
            'priority': self.request.GET.get('priority'),
            'category': self.request.GET.get('category'),
            'search': self.request.GET.get('search'),
            'sort_by': self.request.GET.get('sort_by'),
        }
        context['filter_params'] = {k: v for k,v in get_params.items() if v}
        return context
        
        


# @login_required
# def tasks_list(request):
#     tasks = Tasks.objects.filter(user=request.user).prefetch_related('category', 'subtasks')

#     """Get params"""
#     get_params ={
#         'status': request.GET.get('status'),
#         'priority': request.GET.get('priority'),
#         'category': request.GET.get('category'),
#         'search': request.GET.get('search'),
#         'sort_by': request.GET.get('sort_by'),
#     }
#     filter_params = {k: v for k, v in get_params.items() if v}

#     """Filter"""
#     if get_params['status'] == 'completed':
#         tasks = tasks.filter(is_active=False)
#     if get_params['priority']:
#         tasks = tasks.filter(priority=get_params['priority'])
#     if get_params['category']:
#         tasks = tasks.filter(category__id=get_params['category'])
#     if get_params['search']:
#         tasks = tasks.filter(Q(title__icontains=get_params['search']) | Q(description__icontains=get_params['search']))    

#     """Annotating"""
#     tasks = tasks.annotate(
#         total=Count('subtasks'),
#         completed=Count('subtasks', filter=Q(subtasks__is_active=False)),
#         percent=Case(
#             When(total=0, then=Value(0.0)),
#             default=(F('completed') * 100.0 / F('total')),
#             output_field=FloatField()
#         )
#     )

#     """Sorting"""
#     sort_fields = {
#         'priority_desc': '-priority',
#         'priority_asc': 'priority',
#         'created_desc': '-created_at',
#         'created_asc': 'created_at',
#     }
#     if get_params['sort_by'] in sort_fields:
#         tasks = tasks.order_by(sort_fields[get_params['sort_by']])

#     """Pagination"""
#     tasks = tasks.order_by('-created_at') #Фильтрация уже есть в моделях, дублировал тут только для того, чтоб ушла ошибка в pytest
#     paginator = Paginator(tasks, 5)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     """Context"""
#     context = {
#         'page': page_obj,
#         'categories': Categories.objects.filter(user=request.user),
#         'subform': SubtasksForm(),
#         'filter_params': filter_params,
#     }

#     return render(request, 'todo/tasks_list.html', context)


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
        old_toggle = task.is_active
        task.is_active = not task.is_active
        if old_toggle is True:
            task.completed_at = timezone.now()
        else:
            task.completed_at = None
        task.save()
    return redirect('tasks_list')


@login_required
def task_delete(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Tasks, pk=pk, user=request.user)
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
