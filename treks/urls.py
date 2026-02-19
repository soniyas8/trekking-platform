from django.urls import path
from . import views

app_name = 'treks'

urlpatterns = [
    path('', views.home, name='home'),
    path('treks/', views.trek_list, name='trek_list'),
    path('trek/<slug:slug>/', views.trek_detail, name='trek_detail'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
]