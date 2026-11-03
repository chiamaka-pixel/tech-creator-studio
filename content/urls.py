from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    ContentCalendarView, ContentCreateView, ContentDeleteView, ContentDetailView,
    ContentListView, ContentPermanentDeleteView, ContentRestoreView, ContentUpdateView,
    DashboardView, EmptyRecycleBinView, HelpSupportView, RecycleBinView,
    SettingsView, SourceListView, SourceLinkCreateView, SourceLinkDeleteView,
    SourceLinkUpdateView,
)
from .performance_views import ContentPerformanceUpdateView, PerformanceDashboardView

app_name = "content"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="content/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", DashboardView.as_view(), name="dashboard"),
    path("library/", ContentListView.as_view(), name="item_list"),
    path("create/", ContentCreateView.as_view(), name="item_create"),
    path("calendar/", ContentCalendarView.as_view(), name="content_calendar"),
    path("performance/", PerformanceDashboardView.as_view(), name="performance_dashboard"),
    path("sources/", SourceListView.as_view(), name="source_list"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("help/", HelpSupportView.as_view(), name="help_support"),
    path("recycle-bin/", RecycleBinView.as_view(), name="recycle_bin"),
    path("recycle-bin/empty/", EmptyRecycleBinView.as_view(), name="empty_recycle_bin"),
    path("<int:content_pk>/sources/add/", SourceLinkCreateView.as_view(), name="source_create"),
    path("sources/<int:pk>/edit/", SourceLinkUpdateView.as_view(), name="source_edit"),
    path("sources/<int:pk>/delete/", SourceLinkDeleteView.as_view(), name="source_delete"),
    path("<int:content_pk>/performance/", ContentPerformanceUpdateView.as_view(), name="performance_edit"),
    path("<int:pk>/", ContentDetailView.as_view(), name="item_detail"),
    path("<int:pk>/edit/", ContentUpdateView.as_view(), name="item_edit"),
    path("<int:pk>/delete/", ContentDeleteView.as_view(), name="item_delete"),
    path("<int:pk>/restore/", ContentRestoreView.as_view(), name="item_restore"),
    path("<int:pk>/permanent-delete/", ContentPermanentDeleteView.as_view(), name="item_permanent_delete"),
]
