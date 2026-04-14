from django import forms
from .models import Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'mobile', 'dob']   # add more fields if you have
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'})
        }