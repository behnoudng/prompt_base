from .forms import SignUpForm, ProfileUpdateForm, EmailOrUsernameLoginForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)
class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')
    def get_object(self):
        return self.request.user
class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = EmailOrUsernameLoginForm