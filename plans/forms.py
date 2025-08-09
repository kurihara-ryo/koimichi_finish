from django import forms
from .models import Plan

class PlanBasicForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ["title", "pref", "sub_area", "is_public"]
