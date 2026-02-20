from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.management import call_command
from .models import Trek, Inquiry
from .forms import InquiryForm
import os

# Auto-run migrations on first startup
_migrations_run = False
if not _migrations_run:
    try:
        print("=" * 50)
        print("RUNNING MIGRATIONS...")
        print("=" * 50)
        call_command('migrate', '--noinput')
        _migrations_run = True
        print("MIGRATIONS COMPLETE!")
    except Exception as e:
        print(f"Migration error: {e}")


def home(request):
    """Homepage showing featured treks"""
    featured_treks = Trek.objects.filter(is_featured=True, is_active=True)
    context = {
        'featured_treks': featured_treks,
    }
    return render(request, 'treks/home.html', context)

def trek_list(request):
    """Page showing all treks"""
    treks = Trek.objects.filter(is_active=True)
    context = {
        'treks': treks,
    }
    return render(request, 'treks/trek_list.html', context)

def trek_detail(request, slug):
    """Individual trek detail page"""
    trek = get_object_or_404(Trek, slug=slug, is_active=True)
    context = {
        'trek': trek,
    }
    return render(request, 'treks/trek_detail.html', context)

def contact(request):
    """Contact/inquiry page"""
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your inquiry! We will get back to you soon.')
            return redirect('treks:contact')
    else:
        form = InquiryForm()
    
    context = {
        'form': form,
    }
    return render(request, 'treks/contact.html', context)

def about(request):
    """About page"""
    return render(request, 'treks/about.html')