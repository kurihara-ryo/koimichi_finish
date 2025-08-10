from django import forms
from .models import Plan, Spot, TRAVEL_MODES

class PlanBasicForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ["title", "pref", "sub_area", "default_mode"]  # is_publicは除外
        labels = {
            "title": "タイトル",
            "pref": "都道府県",
            "sub_area": "エリア",
            "default_mode": "交通手段",
        }
        widgets = {
            "default_mode": forms.Select(choices=TRAVEL_MODES),
        }

# Spot（店名＋滞在時間）用フォーム
class SpotNameForm(forms.ModelForm):
    STAY_MINUTES_CHOICES = [(i, f"{i}分") for i in range(15, 241, 15)]
    stay_minutes = forms.ChoiceField(
        choices=STAY_MINUTES_CHOICES,
        label="滞在時間（分）",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    name = forms.CharField(
        required=False,
        label="Shop Name",
        widget=forms.TextInput(attrs={"placeholder": "Shop name", "class": "form-control"})
    )
    class Meta:
        model = Spot
        fields = ["name", "stay_minutes"]
        labels = {
            "name": "Shop Name",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Shop name", "class": "form-control"}),
        }

# Spotフォームセット（5個固定、1以上必須、Add/Deleteなし）
SpotFormSet = forms.modelformset_factory(
    Spot,
    form=SpotNameForm,
    extra=5,
    min_num=1,
    max_num=5,
    validate_min=True,
    validate_max=True,
    can_delete=False,
)
