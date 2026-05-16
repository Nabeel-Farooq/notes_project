import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Note(models.Model):
    """
    Main note model.
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes",
    )

    title = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
    )

    content = models.TextField()

    is_public = models.BooleanField(
        default=False,
    )

    share_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["author"]),
            models.Index(fields=["is_public"]),
            models.Index(fields=["created_at"]),
        ]

    def save(self, *args, **kwargs):
        """
        Auto-generate unique slug from title.
        """

        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Note.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title} ({self.author})"


class NoteVersion(models.Model):
    """
    Stores historical versions of notes.
    """

    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name="versions",
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Version of {self.note.title} at {self.created_at}"
