from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"placeholder": "Enter Your Email here"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if "@kristujayanti.com" in email:
            return email
        else:
            raise forms.ValidationError("This is not a valid email ")

    def save(self):
        # Sets username to email before saving
        user = super(RegistrationForm, self).save(commit=False)
        user.save()
        return user
