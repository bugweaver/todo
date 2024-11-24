from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.views import View

from .forms import ListForm, TaskForm
from .models import List, Task
from django.shortcuts import get_object_or_404

from login_required import LoginNotRequiredMixin


class RegisterView(LoginNotRequiredMixin, CreateView):
    form_class = UserCreationForm
    template_name = "core/RegisterPage.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")

        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)
        return response


class CustomLoginView(LoginNotRequiredMixin, LoginView):
    template_name = "core/LoginPage.html"


class HomeView(View):
    def get(self, request):
        lists_of_tasks = List.objects.filter(user=request.user)
        return render(request, 'core/home.html', {'lists_of_tasks': lists_of_tasks})


class CreateListView(View):
    def get(self, request):
        list_form = ListForm()
        task_form = TaskForm()
        context = {
            'list_form': list_form,
            'task_form': task_form,
        }
        return render(request, 'core/CreateListPage.html', context=context)

    def post(self, request):
        list_form = ListForm(request.POST)
        task_form = TaskForm(request.POST)

        if list_form.is_valid() and task_form.is_valid():
            new_list = list_form.save(commit=False)
            new_task = task_form.save(commit=False)

            new_list.user = request.user
            new_task.list_name = new_list

            new_list.save()
            new_task.save()

            tasks = request.POST.getlist('tasks')
            for task_text in tasks:
                if task_text:
                    Task.objects.create(list_name=new_list, text=task_text)

            return redirect('core:home')

        context = {
            'list_form': list_form,
            'task_form': task_form,
        }
        return render(request, 'core/CreateListPage.html', context=context)


class UpdateListView(View):
    def get(self, request, list_id):
        list_instance = get_object_or_404(List, id=list_id)
        list_form = ListForm(instance=list_instance)
        task_form = TaskForm()

        tasks = Task.objects.filter(list_name=list_instance)

        context = {
            'list_form': list_form,
            'task_form': task_form,
            'tasks': tasks,
            'list_id': list_id,
        }
        return render(request, 'core/UpdateListPage.html', context=context)

    def post(self, request, list_id):

        list_instance = get_object_or_404(List, id=list_id)
        list_form = ListForm(request.POST, instance=list_instance)
        task_form = TaskForm(request.POST)

        if list_form.is_valid() and task_form.is_valid():
            list_form.save()

            tasks = request.POST.getlist('tasks')

            if task_form.cleaned_data['text']:
                tasks.append(task_form.cleaned_data['text'])

            for task_text in tasks:
                if task_text:
                    Task.objects.create(list_name=list_instance, text=task_text)

            return redirect(reverse('core:list_detail', kwargs={'pk': list_id}))

        context = {
            'list_form': list_form,
            'task_form': task_form,
            'tasks': Task.objects.filter(list_name=list_instance),
            'list_id': list_id,
        }
        return render(request, 'core/UpdateListPage.html', context=context)


class ListDetailView(DetailView):
    model = List
    template_name = 'core/ListDetailPage.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_completed_tasks'] = self.object.tasks.filter(completed=True).exists()
        context['has_uncompleted_tasks'] = self.object.tasks.filter(completed=False).exists()
        return context

    def post(self, request, *args, **kwargs):
        list_object = self.get_object()

        task_id = request.POST.get('task_id')

        if task_id:
            task = get_object_or_404(Task, id=task_id)

        else:
            task = None

        if 'complete_task' in request.POST:
            task.completed = True
            task.save()

        elif 'delete_task' in request.POST:
            task.delete()

        elif 'edit_task' in request.POST:
            new_text = request.POST.get('new_text')
            task.text = new_text
            task.save()

        elif 'delete_list' in request.POST:
            list_object.delete()
            print('Список удалён')
            return redirect('core:home')

        else:
            task.completed = False
            task.save()

        return redirect(reverse('core:list_detail', kwargs={'pk': list_object.pk}))
