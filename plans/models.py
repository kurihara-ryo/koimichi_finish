from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

PREF_CHOICES = [
    ("東京都", "東京都"),
    ("神奈川県", "神奈川県"),
    ("千葉県", "千葉県"),
    ("埼玉県", "埼玉県"),
]

SUBAREA_CHOICES = [
    ("渋谷", "渋谷"), ("新宿", "新宿"), ("原宿", "原宿"),
    ("高円寺", "高円寺"), ("町田", "町田"), ("浅草", "浅草"),
    ("みなとみらい", "みなとみらい"), ("横浜", "横浜"), ("中山", "中山"),
    ("船橋", "船橋"), ("川越", "川越"),
]

ALLOWED_SUBAREAS_BY_PREF = {
    "東京都": {"渋谷","新宿","原宿","高円寺","町田","浅草"},
    "神奈川県": {"みなとみらい","横浜","中山"},
    "千葉県": {"船橋"},
    "埼玉県": {"川越"},
}

TRAVEL_MODES = [
    ("train", "電車"),
    ("bus", "バス"),
    ("car", "車"),
    ("walk", "徒歩"),
]

class Plan(models.Model):
    title = models.CharField(max_length=100)
    pref = models.CharField(max_length=20, choices=PREF_CHOICES)
    sub_area = models.CharField(max_length=50, choices=SUBAREA_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.pref}/{self.sub_area})"

    def clean(self):
        if self.pref and self.sub_area:
            allowed = ALLOWED_SUBAREAS_BY_PREF.get(self.pref, set())
            if self.sub_area not in allowed:
                raise ValidationError({"sub_area": f"{self.pref} では選べないエリアです。"})


class Spot(models.Model):
    """訪れるスポット（順番つき）"""
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="spots")
    order = models.PositiveIntegerField(help_text="訪問順（1から）")
    name = models.CharField(max_length=100)
    stay_minutes = models.PositiveIntegerField(default=60, help_text="滞在時間(分)")

    class Meta:
        ordering = ["order"]
        unique_together = ("plan", "order")

    def __str__(self):
        return f"{self.order}. {self.name} ({self.stay_minutes}分)"


class Leg(models.Model):
    """スポット間の移動（Spot n → Spot n+1 を想定）"""
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="legs")
    order = models.PositiveIntegerField(help_text="移動順（1から、Spot数-1まで）")
    travel_minutes = models.PositiveIntegerField(default=15, help_text="移動時間(分)")
    mode = models.CharField(max_length=10, choices=TRAVEL_MODES, default="walk")

    class Meta:
        ordering = ["order"]
        unique_together = ("plan", "order")

    def __str__(self):
        return f"{self.order}. {self.get_mode_display()} {self.travel_minutes}分"
