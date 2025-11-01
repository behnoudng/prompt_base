from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
class PromptType(models.TextChoices):
    JSON = 'json', 'JSON'
    MARKDOWN = 'md', 'Markdown'
    TEXT = 'text', 'Plain Text'
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
class Prompt(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    type = models.CharField(
        max_length=10,
        choices=PromptType.choices,
        default=PromptType.TEXT
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='prompts'
    )
    tags = models.ManyToManyField(Tag, related_name='prompts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    def clean(self):
        if self.pk and self.tags.count() < 2:
            raise ValidationError("You must select at least 2 tags.")
    class Meta:
        ordering = ['-created_at']