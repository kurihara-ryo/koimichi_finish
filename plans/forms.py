from django import forms
from .models import Plan, TRAVEL_MODES

class PlanBasicForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ["title", "pref", "sub_area", "default_mode", "is_public"]
        labels = {
            "title": "タイトル",
            "pref": "都道府県",
            "sub_area": "エリア",
            "default_mode": "交通手段",
            "is_public": "公開設定",
        }
        widgets = {
            "default_mode": forms.Select(choices=TRAVEL_MODES),
        }
        