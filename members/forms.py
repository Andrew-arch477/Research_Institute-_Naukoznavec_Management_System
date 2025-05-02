from django import forms
from .models import Schedule, Student, Subject, Teacher, Grade, Class

class StudentForm(forms.Form):
    name = forms.CharField(
        label="Ім'я:",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Ім'я Учня",
            'autofocus': 'autofocus',
        }),
    )

    class_hi_visits = forms.ModelChoiceField(
        label="Який клас відвідує учень:",
        queryset= Class.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )

    surname = forms.CharField(
        label="Прізвище:",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Прізвище учня'
        }),
    )

class TeacherForm_old(forms.Form):
    name = forms.CharField(
        label="Ім'я:",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Ім'я вчителя",
            'autofocus': 'autofocus',
        }),
    )

    surname = forms.CharField(
        label="Прізвище:",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Прізвище вчителя'
        }),
    )

    age = forms.IntegerField(
        label="Вік:",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Вік вчителя'
        }),
    )

    subject = forms.ModelChoiceField(
        label="Предмет який викладає:",
        queryset= Subject.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'surname', 'age', 'subject', 'password']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Ім'я вчителя",
                'autofocus': 'autofocus',
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Прізвище вчителя',
            }),
            'age': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вік вчителя',
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
            }),

            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': "Код для вчителя",
            }),
        }

class Teacher_Login_Form(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'surname', 'password']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Ім'я вчителя",
                'autofocus': 'autofocus',
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Прізвище вчителя',
            }),

            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': "Код для вчителя",
            }),
        }

class SubjectForm(forms.Form):

    name = forms.CharField(
        label="Назва:",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Назва предмету",
            'autofocus': 'autofocus',
        }),
    )

    description = forms.CharField(
        label="Опис:",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Що на ньому викладається'
        }),
    )

class GradeForm(forms.Form):
    date = forms.CharField(
        label="День:",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "День коли отримана оцінка",
            'autofocus': 'autofocus',
        }),
    )

    score = forms.IntegerField(
        label="Оцінка:",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Оцінка'
        }),
    )

    student = forms.ModelChoiceField(
        label="Учень:",
        queryset= Student.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )

    subject = forms.ModelChoiceField(
        label="Предмет:",
        queryset= Subject.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )

class ClassForm(forms.Form):

    name = forms.CharField(
        label="Назва:",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Назва класу",
            'autofocus': 'autofocus',
        }),
    )

    year = forms.IntegerField(
        label="Рік:",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Рік cтворення класу'
        }),
    )

class ScheduleForm(forms.Form):
    day = forms.CharField(
        label="День:",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "День проведення уроку",
            'autofocus': 'autofocus',
        }),
    )

    surname = forms.CharField(
        label="Прізвище:",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Прізвище вчителя'
        }),
    )

    time = forms.IntegerField(
        label="Час:",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Час початку'
        }),
    )

    subject = forms.ModelChoiceField(
        label="Предмет:",
        queryset= Subject.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )

    class_assigned = forms.ModelChoiceField(
        label="Який клас приймає участь:",
        queryset= Class.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )

    teacher = forms.ModelChoiceField(
        label = "Викладач",
        queryset= Teacher.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )






