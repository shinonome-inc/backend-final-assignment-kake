from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
    # list_displayは、管理画面での一覧表示時に表示されるフィールドを指定するオプション
    list_display = ("username", "email", "is_staff", "is_active")  # 邪魔な姓・名を削除


# カスタマイズしたUserAdminを再登録
admin.site.register(User, CustomUserAdmin)
