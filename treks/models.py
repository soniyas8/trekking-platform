from django.db import models
from django.utils.text import slugify

class Trek(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('difficult', 'Difficult'),
        ('extreme', 'Extreme'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, help_text="Brief summary for cards")
    
    # Trek Details
    duration_days = models.IntegerField(help_text="Number of days")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    max_altitude = models.IntegerField(help_text="Maximum altitude in meters")
    best_season = models.CharField(max_length=100, help_text="e.g., March-May, September-November")
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in USD")
    
    # Images
    featured_image = models.ImageField(upload_to='treks/', blank=True, null=True)
    
    # Status
    is_featured = models.BooleanField(default=False, help_text="Show on homepage?")
    is_active = models.BooleanField(default=True, help_text="Is this trek currently offered?")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', 'name']
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class Inquiry(models.Model):
    trek = models.ForeignKey(Trek, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = 'Inquiries'
    
    def __str__(self):
        return f"Inquiry from {self.name} - {self.submitted_at.strftime('%Y-%m-%d')}"