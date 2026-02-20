from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Contact,Package,Section1,Collaboration,Checkout,ServiceHome,Feedback,Brand
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['phone_no', 'email', 'password1', 'password2']

    phone_no = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your Username', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'class': 'form-control'}))

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Your Name *', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Your Email *', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'phone', 'placeholder': 'Your Phone'}),
            'subject': forms.Select(attrs={'class': 'form-control', 'id': 'subject'}, choices=Contact.SUBJECT_CHOICES),
            'message': forms.Textarea(attrs={'class': 'form-control', 'id': 'message', 'placeholder': 'Your Message *', 'required': True}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if not phone.isdigit():
                raise forms.ValidationError("Phone number must contain only digits.")
            if len(phone) != 10:
                raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['name', 'price', 'description', 'features', 'detailed_description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter package name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description'}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter features separated by commas'}),
            'detailed_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Detailed description'}),
        }

class Section1_form(forms.ModelForm):
    class Meta:
        model = Section1
        fields = ['title', 'heading', 'content', 'image', 'button_name', 'button_link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'heading': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'button_name': forms.TextInput(attrs={'class': 'form-control'}),
            'button_link': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CollaborationForm(forms.ModelForm):
    class Meta:
        model = Collaboration
        fields = ['full_name', 'email', 'phone', 'business_name', 'collaboration_type', 'message']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your business name'}),
            'collaboration_type': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your collaboration idea...', 'rows': 4}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone or len(phone) != 10 or not phone.isdigit():
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone
    
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['full_name', 'email', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'maxlength': '10', 
                'pattern': '\d{10}', 
                'title': 'Enter exactly 10 digits'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone or len(phone) != 10 or not phone.isdigit():
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone

class ServiceHomeForm(forms.ModelForm):
    class Meta:
        model = ServiceHome
        fields = ['image', 'heading', 'subheading', 'url']
        widgets = {
            'heading': forms.TextInput(attrs={'class': 'form-control'}),
            'subheading': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'rating','company_type','feedback']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_image', 'brand_name', 'short_description', 'swiggy_url', 'zomato_url']

        widgets = {
            'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Brand Name'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Short Description'}),
            'swiggy_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter Swiggy URL'}),
            'zomato_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter Zomato URL'}),
            'brand_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }