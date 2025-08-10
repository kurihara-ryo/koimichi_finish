from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib import messages
from .models import Plan

@require_POST
@login_required
def bulk_delete(request):
    ids = request.POST.getlist("selected")  # <input type="checkbox" name="selected" value="{{ plan.id }}">
    if not ids:
        messages.warning(request, "削除対象が選択されていません。")
        return redirect("plan_list")

    qs = Plan.objects.filter(pk__in=ids, user=request.user)
    count = qs.count()
    qs.delete()
    messages.success(request, f"{count} 件のプランを削除しました。")
    return redirect("plan_list")

