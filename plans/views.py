from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .forms import PlanBasicForm, SpotFormSet
from .models import Plan, Spot, PREF_CHOICES, SUBAREA_CHOICES

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
    """プラン新規作成（店2軒限定）"""
    if request.method == "POST":
        form = PlanBasicForm(request.POST)
        formset = SpotFormSet(request.POST, queryset=Spot.objects.none())
        if form.is_valid() and formset.is_valid():
            plan = form.save(commit=False)
            plan.author = request.user
            plan.save()
            spots = formset.save(commit=False)
            order = 1
            for spot in spots:
                if spot.name:  # 店名が空でなければ保存
                    spot.plan = plan
                    spot.order = order
                    spot.save()
                    order += 1
            messages.success(request, "プランを作成しました。")
            return redirect("plan_detail", pk=plan.pk)
    else:
        form = PlanBasicForm()
        formset = SpotFormSet(queryset=Spot.objects.none())
    return render(request, "plans/plan_form.html", {"form": form, "formset": formset})

def plan_detail(request, pk):
    """プラン詳細"""
    plan = get_object_or_404(Plan, pk=pk)
    return render(request, "plans/plan_detail.html", {"plan": plan})

def plan_list(request):
    """プラン一覧＆検索"""
    pref = request.GET.get("pref", "")
    sub_area = request.GET.get("sub_area", "")

    # デフォルトは全プラン表示
    qs = Plan.objects.all().order_by("-created_at")
    if pref:
        qs = qs.filter(pref=pref)
    if sub_area:
        qs = qs.filter(sub_area=sub_area)

    # 日表示・非表示切替
    if request.method == "POST":
        if request.POST.get("display_mode") == "day":
            request.session["plan_display_mode"] = "day"
        if request.POST.get("hide_listed") == "1":
            # 現在リストにあるプランIDをセッションに保存
            request.session["hidden_plan_ids"] = [p.id for p in qs]
    display_mode = request.session.get("plan_display_mode", "list")
    hidden_plan_ids = request.session.get("hidden_plan_ids", [])
    # 非表示指定があれば除外
    if hidden_plan_ids:
        qs = qs.exclude(id__in=hidden_plan_ids)

    # ボタン表示制御用（必要に応じてTrue/Falseを切り替え）
    context = {
        "plans": qs,
        "pref": pref,
        "sub_area": sub_area,
        "PREF_CHOICES": PREF_CHOICES,
        "SUBAREA_CHOICES": SUBAREA_CHOICES,
        "display_mode": display_mode,
        "show_display_buttons": False,  
        "show_day_button": True,     # !!!!今までの予定のみ非表示ボタンTRUEで消す!!!!!
        "show_hide_button": True,     
    }
    return render(request, "plans/plan_list.html", context)

def logout_view(request):
    # セッションを完全クリアしてからlogout
    request.session.flush()
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

