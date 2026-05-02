# Generated manually for GreenWatch MVP
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='EnvironmentalIndicator',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('name', models.CharField(max_length=120)),('value', models.CharField(max_length=80)),('status', models.CharField(default='stable', max_length=30)),('icon', models.CharField(default='🌿', max_length=10)),('measured_at', models.DateTimeField(auto_now_add=True))],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('title', models.CharField(max_length=140)),('category', models.CharField(choices=[('fire', 'Forest fire / smoke'), ('logging', 'Illegal logging'), ('water_leak', 'Water leak / infrastructure'), ('pollution', 'Pollution / waste'), ('drought', 'Water scarcity / drought impact'), ('wildlife', 'Wildlife or ecosystem damage'), ('other', 'Other')], max_length=30)),('severity', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], default='medium', max_length=15)),('description', models.TextField()),('location_name', models.CharField(max_length=180)),('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),('reporter_name', models.CharField(blank=True, help_text='Optional', max_length=100)),('reporter_contact', models.CharField(blank=True, help_text='Optional email or phone for follow-up', max_length=120)),('attachment', models.FileField(blank=True, upload_to='reports/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'mp4', 'mov', 'pdf'])])),('status', models.CharField(choices=[('pending', 'Pending review'), ('verified', 'Verified'), ('in_progress', 'In progress'), ('resolved', 'Resolved'), ('rejected', 'Rejected')], default='pending', max_length=20)),('authority_note', models.TextField(blank=True)),('public_token', models.CharField(blank=True, max_length=20, unique=True)),('is_public', models.BooleanField(default=False, help_text='Visible on public map after verification')),('created_at', models.DateTimeField(auto_now_add=True)),('updated_at', models.DateTimeField(auto_now=True)),('reporter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='incidents', to=settings.AUTH_USER_MODEL))],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('role', models.CharField(choices=[('citizen', 'Citizen'), ('authority', 'Authority')], default='citizen', max_length=20)),('organization', models.CharField(blank=True, max_length=120)),('phone', models.CharField(blank=True, max_length=30)),('created_at', models.DateTimeField(auto_now_add=True)),('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL))],
        ),
        migrations.CreateModel(
            name='StatusUpdate',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('status', models.CharField(choices=[('pending', 'Pending review'), ('verified', 'Verified'), ('in_progress', 'In progress'), ('resolved', 'Resolved'), ('rejected', 'Rejected')], max_length=20)),('note', models.TextField(blank=True)),('created_at', models.DateTimeField(auto_now_add=True)),('incident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='incidents.incident')),('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL))],
            options={'ordering': ['-created_at']},
        ),
    ]
