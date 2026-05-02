from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from incidents.models import UserProfile, Incident, EnvironmentalIndicator, StatusUpdate

class Command(BaseCommand):
    help = 'Create demo authority, indicators, and sample incidents.'
    def handle(self, *args, **kwargs):
        authority, _ = User.objects.get_or_create(username='authority', defaults={'email':'authority@greenwatch.local', 'is_staff':True})
        authority.set_password('Authority@12345'); authority.save()
        UserProfile.objects.get_or_create(user=authority, defaults={'role':UserProfile.Role.AUTHORITY, 'organization':'Ifrane Environmental Authority'})
        for name,value,status,icon in [('Water availability','Good','snowfall recovery','💧'),('Forest fire risk','Low','humid season','🔥'),('Forest health','Watch','human activity zones','🌲'),('Infrastructure alerts','Medium','pipes and reservoirs','🚰')]:
            EnvironmentalIndicator.objects.get_or_create(name=name, defaults={'value':value,'status':status,'icon':icon})
        samples=[('Smoke near cedar forest','fire','high','Azrou cedar forest',33.433,-5.221,True,'verified'),('Water leak near road','water_leak','medium','Ifrane center',33.533,-5.106,True,'in_progress'),('Illegal dumping near stream','pollution','medium','Ain Vittel area',33.522,-5.094,False,'pending')]
        for title,cat,sev,loc,lat,lng,pub,status in samples:
            inc, created = Incident.objects.get_or_create(title=title, defaults={'category':cat,'severity':sev,'description':'Demo incident for MVP presentation.','location_name':loc,'latitude':lat,'longitude':lng,'is_public':pub,'status':status})
            if created:
                StatusUpdate.objects.create(incident=inc,status=inc.status,note='Demo record created.',updated_by=authority)
        self.stdout.write(self.style.SUCCESS('Demo ready. Authority login: authority / Authority@12345'))
