from django import forms
from .models import ProfileStudent, ProfileTeacher

class ProfileStudentForm(forms.ModelForm):
    class Meta:
        model = ProfileStudent
        fields = [
            'institute', 'course', 'group',
            'skills', 'bio', 'phone',
            'telegram', 'github', 'portfolio'
        ]
        widgets = {
            'institute': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Институт информационных систем'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'group': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: ИС-21-1'}),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Например: Python, Django, React, UI/UX Design, Project Management'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Расскажите о своих интересах, достижениях, опыте участия в проектах...'
            }),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'telegram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@username'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/username'}),
            'portfolio': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://your-portfolio.com'}),
        }
        labels = {
            'institute': 'Институт/Факультет',
            'course': 'Курс',
            'group': 'Группа',
            'skills': 'Навыки и компетенции',
            'bio': 'О себе',
            'phone': 'Телефон',
            'telegram': 'Telegram',
            'github': 'GitHub',
            'portfolio': 'Портфолио',
        }

class ProfileTeacherForm(forms.ModelForm):
    class Meta:
        model = ProfileTeacher
        fields = [
            'department', 'position', 'academic_degree',
            'expertise', 'bio', 'phone', 'office'
        ]
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Кафедра информационных систем'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Старший преподаватель'}),
            'academic_degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Кандидат технических наук'}),
            'expertise': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ваши основные направления исследований и экспертизы...'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Научные интересы, публикации, достижения...'
            }),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'office': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: А-101'}),
        }
        labels = {
            'department': 'Кафедра',
            'position': 'Должность',
            'academic_degree': 'Ученая степень',
            'expertise': 'Области экспертизы',
            'bio': 'Биография',
            'phone': 'Телефон',
            'office': 'Кабинет',
        }