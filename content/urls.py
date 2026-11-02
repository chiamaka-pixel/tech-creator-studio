from django.urls import path

from .views import (
    ContentCalendarView,
    ContentCreateView,
    ContentDeleteView,
    ContentDetailView,
    ContentListView,
    ContentPermanentDeleteView,
    ContentRestoreView,
    ContentUpdateView,
    EmptyRecycleBinView,
    RecycleBinView,
    SourceLinkCreateView,
    SourceLinkDeleteView,
    SourceLinkUpdateView,
)

from .performance_views import (
    ContentPerformanceUpdateView,
    PerformanceDashboardView,
)


app_name = "content"

urlpatterns = [
    # Dashboard
    path("", ContentListView.as_view(), name="item_list"),

    # Create content
    path("create/", ContentCreateView.as_view(), name="item_create"),

    # Content Calendar
    path(
        "calendar/",
        ContentCalendarView.as_view(),
        name="content_calendar",
    ),

    # Performance Dashboard
    path(
        "performance/",
        PerformanceDashboardView.as_view(),
        name="performance_dashboard",
    ),

    # Recycle Bin
    path("recycle-bin/", RecycleBinView.as_view(), name="recycle_bin"),

    path(
        "recycle-bin/empty/",
        EmptyRecycleBinView.as_view(),
        name="empty_recycle_bin",
    ),

    # Source Links
    path(
        "<int:content_pk>/sources/add/",
        SourceLinkCreateView.as_view(),
        name="source_create",
    ),

    path(
        "sources/<int:pk>/edit/",
        SourceLinkUpdateView.as_view(),
        name="source_edit",
    ),

    path(
        "sources/<int:pk>/delete/",
        SourceLinkDeleteView.as_view(),
        name="source_delete",
    ),

    # Individual Content Performance
    path(
        "<int:content_pk>/performance/",
        ContentPerformanceUpdateView.as_view(),
        name="performance_edit",
    ),

    # Individual Content Items
    path("<int:pk>/", ContentDetailView.as_view(), name="item_detail"),

    path("<int:pk>/edit/", ContentUpdateView.as_view(), name="item_edit"),

    path("<int:pk>/delete/", ContentDeleteView.as_view(), name="item_delete"),

    path(
        "<int:pk>/restore/",
        ContentRestoreView.as_view(),
        name="item_restore",
    ),

    path(
        "<int:pk>/permanent-delete/",
        ContentPermanentDeleteView.as_view(),
        name="item_permanent_delete",
    ),
]