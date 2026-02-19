from django.contrib import admin
from .models import Trek, Inquiry 

@admin.register(Trek)
class TrekAdmin(admin.ModelAdmin):
    list_display = ['name', 'difficulty', 'duration_days', 'price', 'is_featured', 'is_active']
    list_filter = ['difficulty', 'is_featured', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active']

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'trek', 'submitted_at']
    list_filter = ['trek', 'submitted_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['submitted_at']
    
    def has_add_permission(self, request):
        #Not allowing adding inquiries through admin (only through form)
        return False