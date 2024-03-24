from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from articles.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "is_pinned"]
    search_fields = ["title"]
    list_filter = ["is_pinned"]
    formfield_overrides = {models.JSONField: {"widget": JSONEditorWidget}}
