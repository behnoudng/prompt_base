from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('profile_picture', 'bio')
