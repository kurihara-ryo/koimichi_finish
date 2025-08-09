from django.contrib import admin
from django.contrib import admin
from .models import Plan, Spot, Leg

class SpotInline(admin.TabularInline):
    model = Spot
    extra = 0


class LegInline(admin.TabularInline):
    model = Leg
    extra = 0


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "pref", "sub_area", "author", "is_public", "created_at")
    list_filter = ("pref", "sub_area", "is_public", "created_at")
    search_fields = ("title", "sub_area", "author__username")
    inlines = [SpotInline, LegInline]


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ("id", "plan", "order", "name", "stay_minutes")
    list_filter = ("plan",)
    search_fields = ("name",)


@admin.register(Leg)
class LegAdmin(admin.ModelAdmin):
    list_display = ("id", "plan", "order", "mode", "travel_minutes")
    list_filter = ("mode", "plan")
