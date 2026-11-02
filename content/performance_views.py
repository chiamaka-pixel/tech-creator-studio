from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from .models import ContentItem, ContentPerformance
from .performance_forms import ContentPerformanceForm


class ContentPerformanceUpdateView(LoginRequiredMixin, View):
    template_name = "content/performance_form.html"

    def get_content_item(self):
        return get_object_or_404(
            ContentItem,
            pk=self.kwargs["content_pk"],
            is_deleted=False,
        )

    def get_performance(self, item):
        try:
            return item.performance
        except ContentPerformance.DoesNotExist:
            return ContentPerformance(content_item=item)

    def get(self, request, *args, **kwargs):
        item = self.get_content_item()
        performance = self.get_performance(item)

        form = ContentPerformanceForm(instance=performance)

        return render(
            request,
            self.template_name,
            {
                "item": item,
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        item = self.get_content_item()
        performance = self.get_performance(item)

        form = ContentPerformanceForm(
            request.POST,
            instance=performance,
        )

        if form.is_valid():
            form.save()
            return redirect(
                "content:item_detail",
                pk=item.pk,
            )

        return render(
            request,
            self.template_name,
            {
                "item": item,
                "form": form,
            },
            status=400,
        )


class PerformanceDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "content/performance_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        records = ContentPerformance.objects.filter(
            content_item__is_deleted=False
        ).select_related("content_item")

        totals = records.aggregate(
            total_reach=Sum("reach"),
            total_views=Sum("views"),
            total_likes=Sum("likes"),
            total_comments=Sum("comments"),
            total_shares=Sum("shares"),
        )

        for key, value in totals.items():
            totals[key] = value or 0

        total_interactions = (
            totals["total_likes"]
            + totals["total_comments"]
            + totals["total_shares"]
        )

        if totals["total_reach"] > 0:
            overall_engagement_rate = (
                total_interactions / totals["total_reach"]
            ) * 100
        else:
            overall_engagement_rate = 0

        record_list = list(records)

        top_records = sorted(
            record_list,
            key=lambda record: (
                record.engagement_rate,
                record.total_interactions,
            ),
            reverse=True,
        )[:5]

        highest_interactions = max(
            (record.total_interactions for record in record_list),
            default=0,
        )

        top_posts = []

        for record in top_records:
            if highest_interactions > 0:
                bar_width = (
                    record.total_interactions
                    / highest_interactions
                ) * 100
            else:
                bar_width = 0

            top_posts.append({
                "item": record.content_item,
                "reach": record.reach,
                "engagement_rate": record.engagement_rate,
                "total_interactions": record.total_interactions,
                "bar_width": round(bar_width, 1),
            })

        metrics = [
            {"label": "Reach", "value": totals["total_reach"]},
            {"label": "Views", "value": totals["total_views"]},
            {"label": "Likes", "value": totals["total_likes"]},
            {"label": "Comments", "value": totals["total_comments"]},
            {"label": "Shares", "value": totals["total_shares"]},
        ]

        highest_metric = max(
            (metric["value"] for metric in metrics),
            default=0,
        )

        for metric in metrics:
            if highest_metric > 0:
                metric["bar_width"] = (
                    metric["value"] / highest_metric
                ) * 100
            else:
                metric["bar_width"] = 0

        context.update({
            **totals,
            "total_interactions": total_interactions,
            "overall_engagement_rate": round(
                overall_engagement_rate,
                2,
            ),
            "tracked_posts": len(record_list),
            "published_posts": ContentItem.objects.filter(
                is_deleted=False,
                status=ContentItem.Status.PUBLISHED,
            ).count(),
            "metrics": metrics,
            "top_posts": top_posts,
        })

        return context