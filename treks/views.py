from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Trek, Inquiry
from .forms import InquiryForm



def home(request):
    "Homepage showing featured treks"
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
    print(f"Looking for trek with slug: {slug}")
    
    trek = get_object_or_404(Trek, slug=slug, is_active=True)
    print(f"Found trek: {trek.name}")
    print(f"Trek price: {trek.price}")
    print(f"Trek duration: {trek.duration_days}")
    
    context = {
        'trek': trek,
    }
    
    print(f"Context being passed: {context}")  # New debug line
    
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
