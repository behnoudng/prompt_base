from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Prompt, Tag, Bookmark
from .forms import PromptForm

class HomeView(ListView):
    model = Prompt
    template_name = 'home.html'
    context_object_name = 'prompts'
    paginate_by = 20
    
    def get_queryset(self):
        return Prompt.objects.select_related('creator').prefetch_related('tags').all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            bookmarked_ids = Bookmark.objects.filter(user=self.request.user).values_list('prompt_id', flat=True)
            context['bookmarked_ids'] = list(bookmarked_ids)
        else:
            context['bookmarked_ids'] = []
        return context

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
    
    
class BookmarksView(LoginRequiredMixin, ListView):
    model = Bookmark
    template_name = 'bookmarks.html'
    context_object_name = 'bookmarks'
    
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).select_related('prompt__creator').prefetch_related('prompt__tags').order_by('-created_at')

@login_required
@require_POST
def toggle_bookmark(request, pk):
    prompt = get_object_or_404(Prompt, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, prompt=prompt)
    
    if not created:
        bookmark.delete()
        return JsonResponse({'bookmarked': False})
    
    return JsonResponse({'bookmarked': True})