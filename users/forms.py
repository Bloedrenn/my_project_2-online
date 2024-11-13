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
