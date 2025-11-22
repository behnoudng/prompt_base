from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class PromptType(models.TextChoices):
    JSON = 'json', 'JSON'
    MARKDOWN = 'md', 'Markdown'
    TEXT = 'text', 'Text'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Prompt(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    type = models.CharField(max_length=10, choices=PromptType.choices, default=PromptType.TEXT)
    tags = models.ManyToManyField(Tag, related_name='prompts')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prompts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def clean(self):
        super().clean()
        if self.pk: 
            tag_count = self.tags.count()
            if tag_count < 2:
                raise ValidationError("A prompt must have at least 2 tags.")
            if tag_count > 4:
                raise ValidationError("A prompt can have at most 4 tags.")
