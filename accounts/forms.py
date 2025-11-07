from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import User

class EmailOrUsernameLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")
    def clean(self):
        username_or_email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username_or_email and password:
            if "@" in username_or_email:
                try:
                    user = User.objects.get(email__iexact=username_or_email)
                    username = user.username
                except User.DoesNotExist:
                    raise forms.ValidationError("No account found.")
            else:
                username = username_or_email
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError("Invalid credentials.")
        return self.cleaned_data
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('profile_picture', 'bio')
