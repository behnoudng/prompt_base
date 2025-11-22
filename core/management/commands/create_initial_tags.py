from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Tag

class Command(BaseCommand):
    help = 'Creates initial set of tags for PromptBase'

    def handle(self, *args, **kwargs):
        tags_data = [
            # AI Models
            'ChatGPT',
            'Claude',
            'GPT-5.1',
            'Gemini',
            'Llama',
            
            # Use Cases
            'Writing',
            'Coding',
            'Creative',
            'Business',
            'Education',
            'Research',
            'Analysis',
            'Translation',
            
            # Content Types
            'Blogging',
            'Email',
            'Documentation',
            
            # Technical
            'Python',
            'JavaScript',
            'Web Dev',
            'Data Science',
            'Debugging',
            
            # Creative
            'Brainstorming',
            'Design',
            
            # Professional
            'Resume',
            'Cover Letter',
            'Presentation',
            
            # Other
            'Productivity',
            'Learning',
            'Fun',
            'Experimental',
        ]
        
        created = 0
        existing = 0
        
        for tag_name in tags_data:
            slug = slugify(tag_name)
            tag, was_created = Tag.objects.get_or_create(
                slug=slug,
                defaults={'name': tag_name}
            )
            
            if was_created:
                created += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created tag: {tag_name}')
                )
            else:
                existing += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nDone! Created {created} new tags. {existing} already existed.'
            )
        )
