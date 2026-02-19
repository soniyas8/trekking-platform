from django import forms
from .models import Inquiry, Trek

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['trek', 'name', 'email', 'phone', 'message']
        widgets = {
            'trek': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-sage-200 focus:border-sage-400 focus:ring focus:ring-sage-200 focus:ring-opacity-50'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-sage-200 focus:border-sage-400 focus:ring focus:ring-sage-200 focus:ring-opacity-50',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-sage-200 focus:border-sage-400 focus:ring focus:ring-sage-200 focus:ring-opacity-50',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-sage-200 focus:border-sage-400 focus:ring focus:ring-sage-200 focus:ring-opacity-50',
                'placeholder': '+977 123-456-7890 (optional)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-sage-200 focus:border-sage-400 focus:ring focus:ring-sage-200 focus:ring-opacity-50',
                'placeholder': 'Tell us about your trek plans, questions, or special requirements...',
                'rows': 5
            }),
        }
        labels = {
            'trek': 'Which trek are you interested in?',
            'name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number (Optional)',
            'message': 'Your Message',
        }