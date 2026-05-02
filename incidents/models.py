from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class UserProfile(models.Model):
    class Role(models.TextChoices):
        CITIZEN = 'citizen', 'Citizen'
        AUTHORITY = 'authority', 'Authority'
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CITIZEN)
    organization = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.user.username} - {self.role}'

class Incident(models.Model):
    class Category(models.TextChoices):
        FIRE = 'fire', 'Forest fire / smoke'
        LOGGING = 'logging', 'Illegal logging'
        WATER_LEAK = 'water_leak', 'Water leak / infrastructure'
        POLLUTION = 'pollution', 'Pollution / waste'
        DROUGHT = 'drought', 'Water scarcity / drought impact'
        WILDLIFE = 'wildlife', 'Wildlife or ecosystem damage'
        OTHER = 'other', 'Other'
    class Severity(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        CRITICAL = 'critical', 'Critical'
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending review'
        VERIFIED = 'verified', 'Verified'
        IN_PROGRESS = 'in_progress', 'In progress'
        RESOLVED = 'resolved', 'Resolved'
        REJECTED = 'rejected', 'Rejected'

    title = models.CharField(max_length=140)
    category = models.CharField(max_length=30, choices=Category.choices)
    severity = models.CharField(max_length=15, choices=Severity.choices, default=Severity.MEDIUM)
    description = models.TextField()
    location_name = models.CharField(max_length=180)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    reporter_name = models.CharField(max_length=100, blank=True, help_text='Optional')
    reporter_contact = models.CharField(max_length=120, blank=True, help_text='Optional email or phone for follow-up')
    reporter = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='incidents')
    attachment = models.FileField(upload_to='reports/', blank=True, validators=[FileExtensionValidator(['jpg','jpeg','png','webp','mp4','mov','pdf'])])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    authority_note = models.TextField(blank=True)
    public_token = models.CharField(max_length=20, unique=True, blank=True)
    is_public = models.BooleanField(default=False, help_text='Visible on public map after verification')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self): return f'{self.title} ({self.get_status_display()})'

    def save(self, *args, **kwargs):
        if not self.public_token:
            import secrets
            self.public_token = secrets.token_hex(5).upper()
        super().save(*args, **kwargs)

class StatusUpdate(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='updates')
    status = models.CharField(max_length=20, choices=Incident.Status.choices)
    note = models.TextField(blank=True)
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created_at']

class EnvironmentalIndicator(models.Model):
    name = models.CharField(max_length=120)
    value = models.CharField(max_length=80)
    status = models.CharField(max_length=30, default='stable')
    icon = models.CharField(max_length=10, default='🌿')
    measured_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
