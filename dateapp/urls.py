"""
URL configuration for dateapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from plans import views as pv


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", pv.home, name="home"),
    #認証
    path("login",  auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("register", pv.register, name="register"),
    
    path("plans/new/", pv.plan_new, name="plan_new"), # 新規作成
    path("plans/<int:pk>/", pv.plan_detail, name="plan_detail"), # 詳細表示

    # ...既存
    path("plans/", pv.plan_list, name="plan_list"),  # 一覧＆検索
]
    


