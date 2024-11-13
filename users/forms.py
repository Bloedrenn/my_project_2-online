from django import forms
from core.models import Visit


class VisitUpdateForm(forms.ModelForm):
    class Meta:
        model = Visit

        fields = ['master', 'status', 'comment']

        widgets = {
            'master': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class VisitCreateForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['name', 'phone', 'master', 'services', 'status', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'master': forms.Select(attrs={'class': 'form-control'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
