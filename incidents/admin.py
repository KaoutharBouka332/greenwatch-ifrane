from django.contrib import admin
from .models import Incident, StatusUpdate, EnvironmentalIndicator, UserProfile

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('title','category','severity','status','is_public','created_at')
    list_filter = ('category','severity','status','is_public')
    search_fields = ('title','description','location_name','reporter_contact','public_token')

admin.site.register(StatusUpdate)
admin.site.register(EnvironmentalIndicator)
admin.site.register(UserProfile)
