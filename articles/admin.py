from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from articles.models import Article
from documents import ArticleDocument


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "is_pinned"]
    search_fields = ["title"]
    list_filter = ["is_pinned"]
    formfield_overrides = {models.JSONField: {"widget": JSONEditorWidget}}
    list_per_page = 20

    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return super().get_search_results(request, queryset, search_term)
        es_queryset = ArticleDocument.exact_match(search_term)[:self.list_per_page * 5]
        ids = [hit.meta.id for hit in es_queryset]
        return queryset.filter(pk__in=ids), True


