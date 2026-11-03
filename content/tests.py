from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, ContentItem, ContentPerformance, SourceLink


class ContentPageRenderTests(TestCase):
    """Smoke tests for the pages whose templates share project context."""

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username="studio-test-user",
            password="test-password-123",
        )
        cls.category = Category.objects.create(name="Education")
        cls.item = ContentItem.objects.create(
            title="A test content item",
            category=cls.category,
            audience="Beginner creators",
            research_notes="Research notes for the test.",
            draft_text="A sample draft.",
            caption="A sample caption.",
            planned_date=date.today(),
        )
        cls.source = SourceLink.objects.create(
            content_item=cls.item,
            url="https://example.com/research",
            title="Example research source",
            note="A source note.",
        )
        ContentPerformance.objects.create(
            content_item=cls.item,
            reach=5000,
            views=6200,
            likes=300,
            comments=40,
            shares=30,
        )
        cls.item_without_performance = ContentItem.objects.create(
            title="Content without a performance record",
        )
        cls.deleted_item = ContentItem.objects.create(
            title="Archived content item",
            is_deleted=True,
            deleted_at=timezone.now(),
        )

    def setUp(self):
        self.client.force_login(self.user)

    def assertPageRenders(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, msg=f"Failed URL: {url}; response: {response.status_code}")
        return response

    def test_main_workspace_pages_render(self):
        urls = [
            reverse("content:item_list"),
            reverse("content:item_create"),
            reverse("content:item_edit", args=[self.item.pk]),
            reverse("content:item_detail", args=[self.item.pk]),
            reverse("content:content_calendar"),
            reverse("content:content_calendar") + "?year=2026&month=11",
            reverse("content:performance_dashboard"),
            reverse("content:performance_edit", args=[self.item.pk]),
            reverse("content:recycle_bin"),
            reverse("content:item_delete", args=[self.item.pk]),
            reverse("content:item_permanent_delete", args=[self.deleted_item.pk]),
            reverse("content:source_create", args=[self.item.pk]),
            reverse("content:source_edit", args=[self.source.pk]),
            reverse("content:source_delete", args=[self.source.pk]),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertPageRenders(url)

    def test_detail_page_renders_when_no_performance_record_exists(self):
        response = self.assertPageRenders(
            reverse("content:item_detail", args=[self.item_without_performance.pk])
        )
        self.assertContains(response, "No performance data has been recorded")

    def test_performance_dashboard_uses_dictionary_entries_for_top_posts(self):
        response = self.assertPageRenders(reverse("content:performance_dashboard"))
        self.assertContains(response, "A test content item")
        self.assertContains(response, "5000")

    def test_calendar_renders_scheduled_item_from_week_cells(self):
        response = self.assertPageRenders(reverse("content:content_calendar"))
        self.assertContains(response, "A test content item")

    def test_anonymous_visitors_are_redirected_to_login(self):
        self.client.logout()
        response = self.client.get(reverse("content:performance_dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_content_can_be_moved_to_recycle_bin_and_restored(self):
        delete_url = reverse("content:item_delete", args=[self.item.pk])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)

        self.item.refresh_from_db()
        self.assertTrue(self.item.is_deleted)
        self.assertIsNotNone(self.item.deleted_at)

        restore_url = reverse("content:item_restore", args=[self.item.pk])
        response = self.client.post(restore_url)
        self.assertEqual(response.status_code, 302)

        self.item.refresh_from_db()
        self.assertFalse(self.item.is_deleted)
        self.assertIsNone(self.item.deleted_at)

    def test_archived_content_can_be_permanently_deleted(self):
        delete_url = reverse(
            "content:item_permanent_delete",
            args=[self.deleted_item.pk],
        )
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            ContentItem.objects.filter(pk=self.deleted_item.pk).exists()
        )

    def test_source_can_be_deleted(self):
        delete_url = reverse("content:source_delete", args=[self.source.pk])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(SourceLink.objects.filter(pk=self.source.pk).exists())

    def test_dashboard_settings_help_and_sources_render(self):
        urls = [
            reverse("content:dashboard"),
            reverse("content:settings"),
            reverse("content:help_support"),
            reverse("content:source_list"),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertPageRenders(url)

    def test_login_page_is_available_to_anonymous_visitors(self):
        self.client.logout()
        response = self.client.get(reverse("content:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign in to your studio")

    def test_content_library_search_filters_titles(self):
        response = self.assertPageRenders(reverse("content:item_list") + "?q=test content")
        self.assertContains(response, "A test content item")
        self.assertNotContains(response, "Content without a performance record")

    def test_performance_form_updates_existing_record(self):
        response = self.client.post(
            reverse("content:performance_edit", args=[self.item.pk]),
            {
                "reach": 6000,
                "views": 7000,
                "likes": 350,
                "comments": 50,
                "shares": 40,
                "notes": "Performance test update.",
            },
        )
        self.assertEqual(response.status_code, 302)
        # setUpTestData can leave the reverse OneToOne relation cached on
        # self.item. Query the database directly so this assertion checks
        # the value saved by the POST request, not a stale in-memory object.
        performance = ContentPerformance.objects.get(
            content_item_id=self.item.pk
        )
        self.assertEqual(performance.reach, 6000)
        self.assertEqual(performance.views, 7000)
        self.assertEqual(performance.total_interactions, 440)
        self.assertEqual(performance.notes, "Performance test update.")

