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
    #東京都
    ("渋谷", "渋谷"),
    ("新宿", "新宿"),
    ("原宿", "原宿"),
    ("高円寺", "高円寺"),
    ("町田", "町田"),
    ("浅草", "浅草"),
    
    #神奈川
    ("みなとみらい", "みなとみらい"),
    ("横浜", "横浜"),
    ("中山", "中山"),
    
    # 千葉県
    ("船橋", "船橋"),
    
    # 埼玉県
    ("川越", "川越"),
]

ALLOWED_SUBAREAS_BY_PREF = {
    "東京都": {"渋谷", "新宿", "原宿", "高円寺", "町田", "浅草"},
    "神奈川県": {"みなとみらい", "横浜", "中山"},
    "千葉県": {"船橋"},
    "埼玉県": {"川越"},
}
class Plan(models.Model):
    title = models.CharField(max_length=100)
    pref = models.CharField(max_length=20, choices=PREF_CHOICES)         # 都道府県
    sub_area = models.CharField(max_length=50, choices=SUBAREA_CHOICES)   # エリア（選択式）
    author = models.ForeignKey(User, on_delete=models.CASCADE)            # 投稿者
    is_public = models.BooleanField(default=True)                         # 公開/非公開
    created_at = models.DateTimeField(auto_now_add=True)                  # 作成日時

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.pref} / {self.sub_area})"

    def clean(self):
        # pref と sub_area の組み合わせ整合性チェック
        if self.pref and self.sub_area:
            allowed = ALLOWED_SUBAREAS_BY_PREF.get(self.pref, set())
            if self.sub_area not in allowed:
                raise ValidationError(
                    {"sub_area": f"{self.pref} で選べるエリアではありません。"}
                )

    def save(self, *args, **kwargs):
        # モデル保存時にも検証を走らせる（管理画面・スクリプト経由でも安全）
        self.full_clean()
        return super().save(*args, **kwargs)
