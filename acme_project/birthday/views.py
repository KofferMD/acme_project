from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.http.response import HttpResponse
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from birthday.models import Congratulation

from birthday.models import Birthday
from birthday.forms import BirthdayForm, CongratulationForm
from birthday.utils import calculate_birthday_countdown


class BirthdayListView(ListView):
    model = Birthday
    queryset = Birthday.objects.prefetch_related(
        'tag').select_related('author')
    ordering = '-id'
    paginate_by = 3


class BirthdayMixin:
    model = Birthday


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)


class BirthdayUpdateView(LoginRequiredMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class BirthdayDeleteView(DeleteView, LoginRequiredMixin):
    model = Birthday
    success_url = reverse_lazy('birthday:list')

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)
    


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        return context
    

class CongratulationCreateView(LoginRequiredMixin, CreateView):
    birthday = None
    model = Congratulation
    form_class = CongratulationForm

    def dispatch(self, request, *args, **kwargs):
        self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})


# @login_required
# def add_comment(request, pk):
#     birthday = get_object_or_404(Birthday, pk=pk)
#     form = CongratulationForm(request.POST)

#     if form.is_valid():
#         # Создаём объект поздравления, но не сохраняем его в БД.
#         congratulation = form.save(commit=False)
#         # В поле author передаём объект автора поздравления.
#         congratulation.author = request.user
#         # В поле birthday передаём объект дня рождения.
#         congratulation.birthday = birthday
#         congratulation.save()
#     return redirect('birthday:detail', pk=pk)




# def birthday(request, pk=None):

#     if pk is not None:
#         instance = get_object_or_404(Birthday, pk=pk)
#     else:
#         instance = None
    
#     form = BirthdayForm(request.POST or None, 
#                         files=request.FILES or None,
#                         instance=instance)
#     context = {'form': form}

#     if form.is_valid():
#         form.save()
#         birthday_countdown = calculate_birthday_countdown(
#             # ...и передаём в неё дату из словаря cleaned_data.
#             form.cleaned_data['birthday']
#         )
#         context.update({'birthday_countdown': birthday_countdown})

#     return render(request, 'birthday/birthday.html', context=context)


# def birthday_list(request):
#     birthdays = Birthday.objects.order_by('id')
#     paginator = Paginator(birthdays, 2)

#     page_number = request.GET.get('page')

#     page_obj = paginator.get_page(page_number)

#     context = {'page_obj': page_obj}

#     return render(request, 
#            'birthday/birthday_list.html',
#            context)


# def delete_birthday(request, pk):
#     instance = get_object_or_404(Birthday, pk=pk)
#     form = BirthdayForm(instance=instance)
#     context = {'form': form}

#     if request.method == 'POST':
#         instance.delete()
#         return redirect('birthday:list')
#     return render(request, 'birthday/birthday.html', context)



