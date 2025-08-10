from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

PREF_CHOICES = [
    ("全国", "全国"),
    ("北海道", "札幌市"),
    ("青森県", "青森市"),
    ("岩手県", "盛岡市"),
    ("宮城県", "仙台市"),
    ("秋田県", "秋田市"),
    ("山形県", "山形市"),
    ("福島県", "福島市"),
    ("茨城県", "水戸市"),
    ("栃木県", "宇都宮市"),
    ("群馬県", "前橋市"),
    ("埼玉県", "さいたま市"),
    ("千葉県", "千葉市"),
    ("東京都", "新宿区"),
    ("神奈川県", "横浜市"),
    ("新潟県", "新潟市"),
    ("富山県", "富山市"),
    ("石川県", "金沢市"),
    ("福井県", "福井市"),
    ("山梨県", "甲府市"),
    ("長野県", "長野市"),
    ("岐阜県", "岐阜市"),
    ("静岡県", "静岡市"),
    ("愛知県", "名古屋市"),
    ("三重県", "津市"),
    ("滋賀県", "大津市"),
    ("京都府", "京都市"),
    ("大阪府", "大阪市"),
    ("兵庫県", "神戸市"),
    ("奈良県", "奈良市"),
    ("和歌山県", "和歌山市"),
    ("鳥取県", "鳥取市"),
    ("島根県", "松江市"),
    ("岡山県", "岡山市"),
    ("広島県", "広島市"),
    ("山口県", "山口市"),
    ("徳島県", "徳島市"),
    ("香川県", "高松市"),
    ("愛媛県", "松山市"),
    ("高知県", "高知市"),
    ("福岡県", "福岡市"),
    ("佐賀県", "佐賀市"),
    ("長崎県", "長崎市"),
    ("熊本県", "熊本市"),
    ("大分県", "大分市"),
    ("宮崎県", "宮崎市"),
    ("鹿児島県", "鹿児島市"),
    ("沖縄県", "那覇市"),
]

SUBAREA_CHOICES = [
    ("札幌駅", "札幌駅"), ("仙台駅", "仙台駅"), ("東京駅", "東京駅"),
    ("新宿駅", "新宿駅"), ("渋谷駅", "渋谷駅"), ("池袋駅", "池袋駅"),
    ("横浜駅", "横浜駅"), ("名古屋駅", "名古屋駅"), ("京都駅", "京都駅"),
    ("大阪駅", "大阪駅"), ("天王寺駅", "天王寺駅"), ("神戸駅", "神戸駅"),
    ("広島駅", "広島駅"), ("博多駅", "博多駅"), ("那覇空港駅", "那覇空港駅"),
]

ALLOWED_SUBAREAS_BY_PREF = {
"全国": {s[0] for s in SUBAREA_CHOICES},
    "東京都": {"東京駅", "新宿駅", "渋谷駅", "池袋駅"},
    "神奈川県": {"横浜駅"},
    "愛知県": {"名古屋駅"},
    "京都府": {"京都駅"},
    "大阪府": {"大阪駅", "天王寺駅"},
    "兵庫県": {"神戸駅"},
    "広島県": {"広島駅"},
    "福岡県": {"博多駅"},
    "沖縄県": {"那覇空港駅"},
    # 必要に応じて追加
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
    default_mode = models.CharField(
        max_length=10,
        choices=TRAVEL_MODES,
        default="walk",
        verbose_name="デフォルト移動手段",
    )

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
