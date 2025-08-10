from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

PREF_CHOICES = [
    ("全国", "全国"),
    ("北海道", "北海道"),
    ("青森県", "青森県"),
    ("岩手県", "岩手県"),
    ("宮城県", "宮城県"),
    ("秋田県", "秋田県"),
    ("山形県", "山形県"),
    ("福島県", "福島県"),
    ("茨城県", "茨城県"),
    ("栃木県", "栃木県"),
    ("群馬県", "群馬県"),
    ("埼玉県", "埼玉県"),
    ("千葉県", "千葉県"),
    ("東京都", "東京都"),
    ("神奈川県", "神奈川県"),
    ("新潟県", "新潟県"),
    ("富山県", "富山県"),
    ("石川県", "石川県"),
    ("福井県", "福井県"),
    ("山梨県", "山梨県"),
    ("長野県", "長野県"),
    ("岐阜県", "岐阜県"),
    ("静岡県", "静岡県"),
    ("愛知県", "愛知県"),
    ("三重県", "三重県"),
    ("滋賀県", "滋賀県"),
    ("京都府", "京都府"),
    ("大阪府", "大阪府"),
    ("兵庫県", "兵庫県"),
    ("奈良県", "奈良県"),
    ("和歌山県", "和歌山県"),
    ("鳥取県", "鳥取県"),
    ("島根県", "島根県"),
    ("岡山県", "岡山県"),
    ("広島県", "広島県"),
    ("山口県", "山口県"),
    ("徳島県", "徳島県"),
    ("香川県", "香川県"),
    ("愛媛県", "愛媛県"),
    ("高知県", "高知県"),
    ("福岡県", "福岡県"),
    ("佐賀県", "佐賀県"),
    ("長崎県", "長崎県"),
    ("熊本県", "熊本県"),
    ("大分県", "大分県"),
    ("宮崎県", "宮崎県"),
    ("鹿児島県", "鹿児島県"),
    ("沖縄県", "沖縄県"),
]

SUBAREA_CHOICES = [
    ("札幌駅", "札幌駅"), ("函館駅", "函館駅"), ("旭川駅", "旭川駅"),
    ("青森駅", "青森駅"), ("盛岡駅", "盛岡駅"), ("仙台駅", "仙台駅"),
    ("秋田駅", "秋田駅"), ("山形駅", "山形駅"), ("福島駅", "福島駅"),
    ("水戸駅", "水戸駅"), ("宇都宮駅", "宇都宮駅"), ("高崎駅", "高崎駅"),
    ("大宮駅", "大宮駅"), ("千葉駅", "千葉駅"), ("東京駅", "東京駅"),
    ("新宿駅", "新宿駅"), ("渋谷駅", "渋谷駅"), ("池袋駅", "池袋駅"),
    ("横浜駅", "横浜駅"), ("新潟駅", "新潟駅"), ("富山駅", "富山駅"),
    ("金沢駅", "金沢駅"), ("福井駅", "福井駅"), ("甲府駅", "甲府駅"),
    ("長野駅", "長野駅"), ("岐阜駅", "岐阜駅"), ("静岡駅", "静岡駅"),
    ("名古屋駅", "名古屋駅"), ("津駅", "津駅"), ("大津駅", "大津駅"),
    ("京都駅", "京都駅"), ("大阪駅", "大阪駅"), ("天王寺駅", "天王寺駅"),
    ("神戸駅", "神戸駅"), ("奈良駅", "奈良駅"), ("和歌山駅", "和歌山駅"),
    ("鳥取駅", "鳥取駅"), ("松江駅", "松江駅"), ("岡山駅", "岡山駅"),
    ("広島駅", "広島駅"), ("山口駅", "山口駅"), ("徳島駅", "徳島駅"),
    ("高松駅", "高松駅"), ("松山駅", "松山駅"), ("高知駅", "高知駅"),
    ("博多駅", "博多駅"), ("佐賀駅", "佐賀駅"), ("長崎駅", "長崎駅"),
    ("熊本駅", "熊本駅"), ("大分駅", "大分駅"), ("宮崎駅", "宮崎駅"),
    ("鹿児島中央駅", "鹿児島中央駅"), ("那覇空港駅", "那覇空港駅"),
]

# 県庁所在地と有名駅の対応
ALLOWED_SUBAREAS_BY_PREF = {
    "全国": {
        "札幌駅", "函館駅", "旭川駅", "青森駅", "盛岡駅", "仙台駅", "秋田駅", "山形駅", "福島駅",
        "水戸駅", "宇都宮駅", "高崎駅", "大宮駅", "千葉駅", "東京駅", "新宿駅", "渋谷駅", "池袋駅",
        "横浜駅", "新潟駅", "富山駅", "金沢駅", "福井駅", "甲府駅", "長野駅", "岐阜駅", "静岡駅",
        "名古屋駅", "津駅", "大津駅", "京都駅", "大阪駅", "天王寺駅", "神戸駅", "奈良駅", "和歌山駅",
        "鳥取駅", "松江駅", "岡山駅", "広島駅", "山口駅", "徳島駅", "高松駅", "松山駅", "高知駅",
        "博多駅", "佐賀駅", "長崎駅", "熊本駅", "大分駅", "宮崎駅", "鹿児島中央駅", "那覇空港駅"
    },

    "北海道": {"札幌駅", "函館駅", "旭川駅", "小樽駅", "釧路駅"},
    "青森県": {"青森駅", "弘前駅", "八戸駅"},
    "岩手県": {"盛岡駅", "一ノ関駅", "釜石駅"},
    "宮城県": {"仙台駅", "石巻駅", "松島海岸駅"},
    "秋田県": {"秋田駅", "大館駅", "横手駅"},
    "山形県": {"山形駅", "米沢駅", "鶴岡駅"},
    "福島県": {"福島駅", "郡山駅", "会津若松駅"},

    "茨城県": {"水戸駅", "つくば駅", "土浦駅"},
    "栃木県": {"宇都宮駅", "日光駅", "小山駅"},
    "群馬県": {"高崎駅", "前橋駅", "草津温泉駅"},
    "埼玉県": {"大宮駅", "川越駅", "秩父駅"},
    "千葉県": {"千葉駅", "舞浜駅", "成田空港駅"},
    "東京都": {"東京駅", "新宿駅", "渋谷駅", "池袋駅", "上野駅", "品川駅"},
    "神奈川県": {"横浜駅", "川崎駅", "鎌倉駅", "小田原駅"},

    "新潟県": {"新潟駅", "長岡駅", "佐渡両津港"},
    "富山県": {"富山駅", "高岡駅"},
    "石川県": {"金沢駅", "和倉温泉駅"},
    "福井県": {"福井駅", "芦原温泉駅"},
    "山梨県": {"甲府駅", "河口湖駅"},
    "長野県": {"長野駅", "松本駅", "軽井沢駅"},
    "岐阜県": {"岐阜駅", "高山駅", "下呂駅"},
    "静岡県": {"静岡駅", "浜松駅", "熱海駅"},
    "愛知県": {"名古屋駅", "金山駅", "豊橋駅"},
    "三重県": {"津駅", "伊勢市駅", "鳥羽駅"},

    "滋賀県": {"大津駅", "彦根駅"},
    "京都府": {"京都駅", "嵯峨嵐山駅", "宇治駅"},
    "大阪府": {"大阪駅", "天王寺駅", "新大阪駅", "なんば駅"},
    "兵庫県": {"神戸駅", "三ノ宮駅", "姫路駅"},
    "奈良県": {"奈良駅", "大和西大寺駅"},
    "和歌山県": {"和歌山駅", "白浜駅"},

    "鳥取県": {"鳥取駅", "米子駅"},
    "島根県": {"松江駅", "出雲市駅"},
    "岡山県": {"岡山駅", "倉敷駅"},
    "広島県": {"広島駅", "宮島口駅", "福山駅"},
    "山口県": {"新山口駅", "下関駅"},

    "徳島県": {"徳島駅", "鳴門駅"},
    "香川県": {"高松駅", "琴平駅"},
    "愛媛県": {"松山駅", "今治駅", "道後温泉駅"},
    "高知県": {"高知駅", "中村駅"},

    "福岡県": {"博多駅", "小倉駅", "天神駅"},
    "佐賀県": {"佐賀駅", "唐津駅"},
    "長崎県": {"長崎駅", "佐世保駅", "ハウステンボス駅"},
    "熊本県": {"熊本駅", "阿蘇駅"},
    "大分県": {"大分駅", "別府駅", "由布院駅"},
    "宮崎県": {"宮崎駅", "日南駅"},
    "鹿児島県": {"鹿児島中央駅", "指宿駅", "霧島神宮駅"},
    "沖縄県": {"那覇空港駅", "美栄橋駅", "首里駅"},
}

PREF_CHOICES_FROM_MAP = [("全国", "全国")] + [
    (p, p) for p in sorted(k for k in ALLOWED_SUBAREAS_BY_PREF.keys() if k != "全国")
]

# 駅（エリア）のchoices：全県の駅をユニオンしてソート
_ALL_STATIONS = sorted({s for v in ALLOWED_SUBAREAS_BY_PREF.values() for s in v})
SUBAREA_CHOICES_FROM_MAP = [(s, s) for s in _ALL_STATIONS]
PREF_CHOICES = PREF_CHOICES_FROM_MAP
SUBAREA_CHOICES = SUBAREA_CHOICES_FROM_MAP

TRAVEL_MODES = [
    ("train", "電車"),
    ("bicycle ","自転車"),
    ("bus", "バス"),
    ("car", "車"),
    ("walk", "徒歩"),
]


class Plan(models.Model):
    title = models.CharField(max_length=100)
    pref = models.CharField(max_length=20, choices=PREF_CHOICES_FROM_MAP)
    sub_area = models.CharField(max_length=50, choices=SUBAREA_CHOICES_FROM_MAP)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    default_mode = models.CharField(
        max_length=10, choices=TRAVEL_MODES, default="walk", verbose_name="デフォルト移動手段"
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
    move_minutes = models.PositiveIntegerField(default=0, null=True, blank=True, help_text="移動時間(分)")

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
