from django import forms
from .models import Prompt, Tag, PromptType

class PromptForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=True,
        help_text="Select between 2-4 tags"
    )
    
    class Meta:
        model = Prompt
        fields = ['title', 'type', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'Give your prompt a descriptive title...'
            }),
            'type': forms.Select(attrs={
                'class': 'form-select bg-dark text-white border-secondary',
                'id': 'promptType'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-secondary font-monospace',
                'rows': 15,
                'id': 'promptContent',
                'placeholder': 'Enter your prompt here...'
            }),
        }
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if not tags:
            raise forms.ValidationError("Please select at least 2 tags.")
        
        tag_count = len(tags)
        if tag_count < 2:
            raise forms.ValidationError("Please select at least 2 tags.")
        if tag_count > 4:
            raise forms.ValidationError("You can select at most 4 tags.")
        
        return tags
