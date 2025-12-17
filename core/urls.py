from django.urls import path
from .views import HomeView, AboutView, PromptCreateView, prompt_detail_ajax, MyPromptsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('my_prompts/', MyPromptsView.as_view(), name='my_prompts'),
    path('prompt/add/', PromptCreateView.as_view(), name='prompt_add'),
    path('prompt/<int:pk>/detail/', prompt_detail_ajax, name='prompt_detail_ajax'),
]
