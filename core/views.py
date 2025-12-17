from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Prompt, Tag
from .forms import PromptForm

class HomeView(ListView):
    model = Prompt
    template_name = 'home.html'
    context_object_name = 'prompts'
    paginate_by = 20
    
    def get_queryset(self):
        return Prompt.objects.select_related('creator').prefetch_related('tags').all()

class AboutView(TemplateView):
    template_name = 'about.html'

class PromptCreateView(LoginRequiredMixin, CreateView):
    model = Prompt
    form_class = PromptForm
    template_name = 'prompt_add.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

def prompt_detail_ajax(request, pk):
    # ajax endpoint
    prompt = get_object_or_404(Prompt.objects.select_related('creator').prefetch_related('tags'), pk=pk)
    
    return JsonResponse({
        'id': prompt.id,
        'title': prompt.title,
        'content': prompt.content,
        'type': prompt.type,
        'creator': prompt.creator.username,
        'created_at': prompt.created_at.strftime('%Y-%m-%d %H:%M'),
        'tags': [tag.name for tag in prompt.tags.all()],
    })

class MyPromptsView(LoginRequiredMixin, ListView):
    model = Prompt
    template_name = 'my_prompts.html'
    context_object_name = 'prompts'

    def get_queryset(self):
        return Prompt.objects.filter(creator=self.request.user)