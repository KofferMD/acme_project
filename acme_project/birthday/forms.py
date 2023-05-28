from django import forms
from .models import Birthday


class BirthdayForm(forms.ModelForm):
    # first_name = forms.CharField(max_length=20, label='Имя')
    # last_name = forms.CharField(required=False,
    #                             label='Фамилия',
    #                             help_text='Необязательное поле')
    # birthday = forms.DateField(label='Дата рождения',
    #                            widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Birthday
        fields = '__all__'
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }

