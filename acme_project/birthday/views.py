from django.shortcuts import get_object_or_404, render
from birthday.models import Birthday
from birthday.forms import BirthdayForm
from birthday.utils import calculate_birthday_countdown


def birthday(request, pk=None):

    if pk is not None:
        instance = get_object_or_404(Birthday, pk=pk)
    else:
        instance = None
    
    form = BirthdayForm(request.POST or None, instance=instance)
    context = {'form': form}

    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            # ...и передаём в неё дату из словаря cleaned_data.
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})

    return render(request, 'birthday/birthday.html', context=context)


def birthday_list(request):
    birthdays = Birthday.objects.all()
    context = {'birthdays': birthdays}
    return render(request, 
           'birthday/birthday_list.html',
           context)

#TODO:delete birthday
