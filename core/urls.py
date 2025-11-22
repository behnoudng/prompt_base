from django.urls import path
from .views import HomeView, AboutView, PromptCreateView, prompt_detail_ajax

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('prompt/add/', PromptCreateView.as_view(), name='prompt_add'),
    path('prompt/<int:pk>/detail/', prompt_detail_ajax, name='prompt_detail_ajax'),
]
