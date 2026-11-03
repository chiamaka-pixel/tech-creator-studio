import calendar
from datetime import date, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q, Sum
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import ContentItemForm
from .models import ContentItem, ContentPerformance, SourceLink
from .source_forms import SourceLinkForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "content/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        items = ContentItem.objects.filter(is_deleted=False)
        performance = ContentPerformance.objects.filter(content_item__is_deleted=False)
        totals = performance.aggregate(
            reach_total=Sum("reach"), likes_total=Sum("likes"),
            comments_total=Sum("comments"), shares_total=Sum("shares"),
        )
        interactions = sum((totals.get(key) or 0) for key in ("likes_total", "comments_total", "shares_total"))
        upcoming = items.filter(planned_date__gte=today).exclude(status=ContentItem.Status.PUBLISHED).order_by("planned_date", "title")[:3]
        month_count = items.filter(planned_date__year=today.year, planned_date__month=today.month).count()
        recent = items.order_by("-updated_at")[:4]
        start = today - timedelta(days=6)
        activity = []
        max_count = 1
        for offset in range(7):
            day = start + timedelta(days=offset)
            count = items.filter(created_at__date=day).count()
            activity.append({"label": day.strftime("%a"), "count": count, "height": 10})
            max_count = max(max_count, count)
        for entry in activity:
            entry["height"] = max(10, round(entry["count"] / max_count * 100))
        context.update({
            "total_content": items.count(),
            "total_reach": totals.get("reach_total") or 0,
            "total_engagement": interactions,
            "scheduled_this_month": month_count,
            "upcoming_items": upcoming,
            "recent_items": recent,
            "activity_days": activity,
        })
        return context


class SourceListView(LoginRequiredMixin, ListView):
    model = SourceLink
    template_name = "content/source_list.html"
    context_object_name = "sources"

    def get_queryset(self):
        return SourceLink.objects.filter(
            content_item__is_deleted=False
        ).select_related("content_item").order_by("-id")


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "content/settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["automation_connected"] = False
        return context


class HelpSupportView(LoginRequiredMixin, TemplateView):
    template_name = "content/help_support.html"


class ContentListView(LoginRequiredMixin, ListView):
    model = ContentItem
    template_name = "content/item_list.html"
    context_object_name = "items"

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(is_deleted=False)
            .select_related("category")
        )
        status = self.request.GET.get("status")
        query = self.request.GET.get("q", "").strip()
        if status in ContentItem.Status.values:
            queryset = queryset.filter(status=status)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(audience__icontains=query)
                | Q(draft_text__icontains=query)
                | Q(caption__icontains=query)
                | Q(hashtags__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = ContentItem.Status.choices
        context["current_status"] = self.request.GET.get("status", "")
        context["search_query"] = self.request.GET.get("q", "")
        return context


class ContentCalendarView(LoginRequiredMixin, TemplateView):
    template_name = "content/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()

        try:
            year = int(self.request.GET.get("year", today.year))
            month = int(self.request.GET.get("month", today.month))
            selected_month = date(year, month, 1)
        except (TypeError, ValueError, OverflowError):
            selected_month = date(today.year, today.month, 1)

        year = selected_month.year
        month = selected_month.month
        calendar_builder = calendar.Calendar(firstweekday=calendar.SUNDAY)
        date_weeks = calendar_builder.monthdatescalendar(year, month)
        first_date = date_weeks[0][0]
        last_date = date_weeks[-1][-1]

        scheduled_items = list(
            ContentItem.objects.filter(
                is_deleted=False,
                planned_date__range=(first_date, last_date),
            )
            .select_related("category")
            .order_by("planned_date", "title")
        )

        items_by_date = {}
        for item in scheduled_items:
            items_by_date.setdefault(item.planned_date, []).append(item)

        weeks = []
        for week in date_weeks:
            week_cells = []
            for current_date in week:
                week_cells.append({
                    "date": current_date,
                    "items": items_by_date.get(current_date, []),
                    "in_month": current_date.month == month,
                    "is_today": current_date == today,
                })
            weeks.append(week_cells)

        if month == 1:
            previous_year, previous_month = year - 1, 12
        else:
            previous_year, previous_month = year, month - 1

        if month == 12:
            next_year, next_month = year + 1, 1
        else:
            next_year, next_month = year, month + 1

        context.update({
            "month_label": selected_month.strftime("%B %Y"),
            "weekdays": [
                "Sunday", "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday",
            ],
            "weeks": weeks,
            "today": today,
            "previous_year": previous_year,
            "previous_month": previous_month,
            "next_year": next_year,
            "next_month": next_month,
            "scheduled_item_count": len(scheduled_items),
        })
        return context


class ContentCreateView(LoginRequiredMixin, CreateView):
    model = ContentItem
    form_class = ContentItemForm
    template_name = "content/item_form.html"
    success_url = reverse_lazy("content:item_list")


class ContentUpdateView(LoginRequiredMixin, UpdateView):
    model = ContentItem
    form_class = ContentItemForm
    template_name = "content/item_form.html"
    success_url = reverse_lazy("content:item_list")

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class ContentDetailView(LoginRequiredMixin, DetailView):
    model = ContentItem
    template_name = "content/item_detail.html"
    context_object_name = "item"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(is_deleted=False)
            .select_related("category", "performance")
            .prefetch_related("sources")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # select_related("performance") makes the one-to-one lookup efficient;
        # getattr's default handles content that has no performance record yet.
        context["performance_record"] = getattr(self.object, "performance", None)
        return context


class ContentDeleteView(LoginRequiredMixin, DeleteView):
    model = ContentItem
    template_name = "content/item_confirm_delete.html"
    success_url = reverse_lazy("content:item_list")

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def form_valid(self, form):
        self.object.is_deleted = True
        self.object.deleted_at = timezone.now()
        self.object.save(update_fields=["is_deleted", "deleted_at", "updated_at"])
        return HttpResponseRedirect(self.get_success_url())


class RecycleBinView(LoginRequiredMixin, ListView):
    model = ContentItem
    template_name = "content/recycle_bin.html"
    context_object_name = "items"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(is_deleted=True)
            .select_related("category")
            .order_by("-deleted_at", "-created_at")
        )


class ContentRestoreView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        item = get_object_or_404(
            ContentItem,
            pk=kwargs["pk"],
            is_deleted=True,
        )
        item.is_deleted = False
        item.deleted_at = None
        item.save(update_fields=["is_deleted", "deleted_at", "updated_at"])
        return redirect("content:recycle_bin")


class ContentPermanentDeleteView(LoginRequiredMixin, DeleteView):
    model = ContentItem
    template_name = "content/item_permanent_delete.html"
    success_url = reverse_lazy("content:recycle_bin")

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)


class EmptyRecycleBinView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        ContentItem.objects.filter(is_deleted=True).delete()
        return redirect("content:recycle_bin")


class SourceLinkCreateView(LoginRequiredMixin, CreateView):
    form_class = SourceLinkForm
    template_name = "content/source_form.html"

    def get_content_item(self):
        return get_object_or_404(
            ContentItem,
            pk=self.kwargs["content_pk"],
            is_deleted=False,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = self.get_content_item()
        return context

    def form_valid(self, form):
        form.instance.content_item = self.get_content_item()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("content:item_detail", kwargs={"pk": self.object.content_item_id})


class SourceLinkUpdateView(LoginRequiredMixin, UpdateView):
    model = SourceLink
    form_class = SourceLinkForm
    template_name = "content/source_form.html"

    def get_queryset(self):
        return SourceLink.objects.filter(
            content_item__is_deleted=False
        ).select_related("content_item")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = self.object.content_item
        return context

    def get_success_url(self):
        return reverse("content:item_detail", kwargs={"pk": self.object.content_item_id})


class SourceLinkDeleteView(LoginRequiredMixin, DeleteView):
    model = SourceLink
    template_name = "content/source_confirm_delete.html"

    def get_queryset(self):
        return SourceLink.objects.filter(
            content_item__is_deleted=False
        ).select_related("content_item")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = self.object.content_item
        return context

    def get_success_url(self):
        return reverse("content:item_detail", kwargs={"pk": self.object.content_item_id})
