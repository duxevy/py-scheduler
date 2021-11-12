from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from .models import Note

TokenAdmin.raw_id_fields = ['user']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    # Поля в списке
    list_display = ("title", "message", "date_add", "public", "important", "author")
    fields = ("date_add", ("title", "public", "important"), "message", "author")
    readonly_fields = ("date_add",)
    search_fields = ["title", "message"]
    list_filter = ("public", "important")

    def save_model(self, request, obj, form, change):
        # Добавление текущего пользователя при сохранении модели
        if not hasattr(obj, 'author') or not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
