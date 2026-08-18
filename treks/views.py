from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Trek, Inquiry
from .forms import InquiryForm
from .route_optimizer import optimize_route
import os
import json


# Auto-run migrations on first startup
_setup_complete = False
if not _setup_complete:
    try:
        print("=" * 50)
        print("RUNNING MIGRATIONS...")
        print("=" * 50)
        call_command('migrate', '--noinput')
        print("MIGRATIONS COMPLETE!")
        
        # Create superuser if it doesn't exist
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            admin_password = os.environ.get('ADMIN_PASSWORD', 'changeme')
            print("Creating superuser...")
            User.objects.create_superuser('admin', 'admin@test.com', admin_password)
            print("Superuser created!")
        
        _setup_complete = True
    except Exception as e:
        print(f"Setup error: {e}")


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


#route optimizer
def optimize_trip(request):
    """Handle multi-trek route optimization"""
    if request.method == 'POST':
        trek_ids = request.POST.getlist('trek_ids')
        # Preserve the order the user selected them in, for the naive comparison
        selected_treks = list(Trek.objects.filter(id__in=trek_ids, is_active=True))
        selected_treks.sort(key=lambda t: trek_ids.index(str(t.id)))

        if len(selected_treks) < 2:
            messages.error(request, 'Please select at least 2 treks to optimize a route.')
            return redirect('treks:trek_list')

        # Naive: distance if visited in the order selected
        from .route_optimizer import haversine_distance
        naive_distance = sum(
            haversine_distance(
                float(selected_treks[i].latitude), float(selected_treks[i].longitude),
                float(selected_treks[i + 1].latitude), float(selected_treks[i + 1].longitude)
            )
            for i in range(len(selected_treks) - 1)
        )

        ordered_treks, total_distance = optimize_route(selected_treks)

        savings = round(naive_distance - total_distance, 1)
        savings_pct = round((savings / naive_distance) * 100, 1) if naive_distance > 0 else 0

        context = {
            'ordered_treks': ordered_treks,
            'total_distance': total_distance,
            'naive_distance': round(naive_distance, 1),
            'savings': savings,
            'savings_pct': savings_pct,
        }
        return render(request, 'treks/optimize_results.html', context)

    return redirect('treks:trek_list')

