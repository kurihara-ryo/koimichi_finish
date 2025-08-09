from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import PlanBasicForm
from .models import Plan, PREF_CHOICES, SUBAREA_CHOICES

def home(request):
    # ログイン状態のテスト表示だけ
    return render(request, "home.html")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # ユーザー作成
            messages.success(request, "登録しました！ログインしてください。")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

@login_required
def plan_new(request):
    """プラン新規作成"""
    if request.method == "POST":
        form = PlanBasicForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.author = request.user
            plan.save()
            messages.success(request, "プランを作成しました。")
            return redirect("plan_detail", pk=plan.pk)
    else:
        form = PlanBasicForm()
    return render(request, "plans/plan_form.html", {"form": form})

def plan_detail(request, pk):
    """プラン詳細"""
    plan = get_object_or_404(Plan, pk=pk)
    return render(request, "plans/plan_detail.html", {"plan": plan})

def plan_list(request):
    """プラン一覧＆検索"""
    pref = request.GET.get("pref", "")
    sub_area = request.GET.get("sub_area", "")

    qs = Plan.objects.filter(is_public=True).order_by("-created_at")
    if pref:
        qs = qs.filter(pref=pref)
    if sub_area:
        qs = qs.filter(sub_area=sub_area)

    return render(request, "plans/plan_list.html", {
        "plans": qs,
        "pref": pref,
        "sub_area": sub_area,
        "PREF_CHOICES": PREF_CHOICES,
        "SUBAREA_CHOICES": SUBAREA_CHOICES,
        
    })
    
    