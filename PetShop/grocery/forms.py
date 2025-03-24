from django import forms
from django.contrib.auth.models import User
from .models import ProductRequest, Supplier
from .models import Profile, PetProfile

class SupplierRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password do not match."
            )

        return cleaned_data

class ProductRequestForm(forms.ModelForm):
    class Meta:
        model = ProductRequest
        fields = ['product_name', 'description']

class SupplierRequestForm(forms.ModelForm):
    class Meta:
        model = ProductRequest
        fields = ['product_name', 'description']

# User Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dob', 'city', 'address', 'contact', 'image']

# Pet Profile Form
class PetProfileForm(forms.ModelForm):
    class Meta:
        model = PetProfile
        fields = ['name', 'breed', 'age', 'image', 'veterinarian', 'visit_date']