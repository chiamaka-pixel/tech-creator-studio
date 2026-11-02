from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ContentItem(models.Model):
    class Format(models.TextChoices):
        TEXT_POST = "text_post", "Text post"
        EDUCATIONAL = "educational", "Educational post"
        POSTER = "poster", "Poster"
        VIDEO_SCRIPT = "video_script", "Video script"

    class Status(models.TextChoices):
        IDEA = "idea", "Idea"
        RESEARCHING = "researching", "Researching"
        DRAFTING = "drafting", "Drafting"
        READY_FOR_REVIEW = "ready_for_review", "Ready for review"
        APPROVED = "approved", "Approved"
        PUBLISHED = "published", "Published"
        NEEDS_REVISION = "needs_revision", "Needs revision"

    class Platform(models.TextChoices):
        FACEBOOK = "facebook", "Facebook"

    title = models.CharField(max_length=200)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items",
    )

    audience = models.CharField(max_length=100, blank=True)

    content_format = models.CharField(
        max_length=20,
        choices=Format.choices,
        default=Format.TEXT_POST,
    )

    research_notes = models.TextField(blank=True)
    draft_text = models.TextField(blank=True)
    caption = models.TextField(blank=True)
    hashtags = models.CharField(max_length=300, blank=True)
    production_notes = models.TextField(blank=True)

    planned_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IDEA,
    )

    platform = models.CharField(
        max_length=20,
        choices=Platform.choices,
        default=Platform.FACEBOOK,
    )

    published_url = models.URLField(blank=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class SourceLink(models.Model):
    content_item = models.ForeignKey(
        ContentItem,
        on_delete=models.CASCADE,
        related_name="sources",
    )

    url = models.URLField()
    title = models.CharField(max_length=200, blank=True)
    published_date = models.DateField(null=True, blank=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return self.title or self.url


class ContentPerformance(models.Model):
    content_item = models.OneToOneField(
        ContentItem,
        on_delete=models.CASCADE,
        related_name="performance",
    )

    reach = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)

    notes = models.TextField(blank=True)

    recorded_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Content Performance"
        verbose_name_plural = "Content Performance"

    def __str__(self):
        return f"Performance: {self.content_item.title}"

    @property
    def total_interactions(self):
        return self.likes + self.comments + self.shares

    @property
    def engagement_rate(self):
        if self.reach == 0:
            return 0

        return (self.total_interactions / self.reach) * 100