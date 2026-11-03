from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, ContentItem, SourceLink


class SourceLinkInline(admin.TabularInline):
    model = SourceLink
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "planned_date", "platform")
    list_filter = ("status", "category", "platform")
    search_fields = ("title", "draft_text")
    inlines = [SourceLinkInline]