from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from .models import Birthday


BEATLES = {'Джон Ленон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}


class BirthdayForm(forms.ModelForm):
    # first_name = forms.CharField(max_length=20, label='Имя')
    # last_name = forms.CharField(required=False,
    #                             label='Фамилия',
    #                             help_text='Необязательное поле')
    # birthday = forms.DateField(label='Дата рождения',
    #                            widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Birthday
        exclude = ('author',)
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.split()[0]
    
    def clean(self):
        super().clean()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']

        if f'{first_name} {last_name}' in BEATLES:
            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )

            raise ValidationError(
                'Мы тоже любим битлз, но введите свое настоящее имя!'
            )

    

