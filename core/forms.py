from django import forms
from .models import ContactMessage, NewsletterSubscriber, Payment

from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'id': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'id': 'email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject',
                'id': 'subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Leave a message here',
                'id': 'message',
                'style': 'height: 150px'
            }),
        }



class NewsletterForm(forms.ModelForm):
    class Meta:
        model   = NewsletterSubscriber
        fields  = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'aria-label': 'Your email'
            }),
        }
        
        
    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Enter a valid email address.")

        # Then check for duplicates
        if NewsletterSubscriber.objects.filter(email=email).exists():
            raise ValidationError("This email is already subscribed.")

        return email
    
    


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name', 'email', 'phone', 'payment_method', 'product_type', 'amount']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Phone Number',
                'id': 'phone-input',  # Important for JS hook
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-control',
            }),
            'product_type': forms.HiddenInput(),
            'amount': forms.HiddenInput(),
        }