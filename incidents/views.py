from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponseForbidden
from .models import Incident, EnvironmentalIndicator, StatusUpdate, UserProfile
from .forms import PublicIncidentForm, AdminIncidentForm


def is_authority(user):
    if not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    return hasattr(user, 'profile') and user.profile.role == UserProfile.Role.AUTHORITY


def home(request):
    stats = {
        'total': Incident.objects.count(),
        'pending': Incident.objects.filter(status=Incident.Status.PENDING).count(),
        'verified': Incident.objects.filter(status=Incident.Status.VERIFIED).count(),
        'resolved': Incident.objects.filter(status=Incident.Status.RESOLVED).count(),
    }
    public_incidents = Incident.objects.filter(is_public=True).exclude(status=Incident.Status.REJECTED)[:6]
    indicators = EnvironmentalIndicator.objects.order_by('-measured_at')[:4]
    return render(request, 'incidents/home.html', {'stats': stats, 'public_incidents': public_incidents, 'indicators': indicators})


def report_incident(request):
    if request.method == 'POST':
        form = PublicIncidentForm(request.POST, request.FILES)
        if form.is_valid():
            incident = form.save(commit=False)
            if request.user.is_authenticated:
                incident.reporter = request.user
            incident.status = Incident.Status.PENDING
            incident.is_public = False
            incident.save()
            StatusUpdate.objects.create(incident=incident, status=incident.status, note='Report submitted and waiting for authority review.', updated_by=request.user if request.user.is_authenticated else None)
            return redirect('thanks', token=incident.public_token)
    else:
        form = PublicIncidentForm()
    return render(request, 'incidents/report.html', {'form': form})


def thanks(request, token):
    incident = get_object_or_404(Incident, public_token=token)
    return render(request, 'incidents/thanks.html', {'incident': incident})


def track(request):
    token = request.GET.get('token', '').strip().upper()
    if token:
        return redirect('track_detail', token=token)
    return render(request, 'incidents/track.html')


def track_detail(request, token):
    incident = get_object_or_404(Incident, public_token=token.upper())
    return render(request, 'incidents/track_detail.html', {'incident': incident})


@login_required
@user_passes_test(is_authority)
def authority_dashboard(request):
    q = request.GET.get('q','')
    status = request.GET.get('status','')
    category = request.GET.get('category','')
    incidents = Incident.objects.all()
    if q:
        incidents = incidents.filter(Q(title__icontains=q)|Q(description__icontains=q)|Q(location_name__icontains=q)|Q(public_token__icontains=q))
    if status:
        incidents = incidents.filter(status=status)
    if category:
        incidents = incidents.filter(category=category)
    counts = Incident.objects.values('status').annotate(total=Count('id'))
    return render(request, 'incidents/authority.html', {'incidents': incidents, 'counts': counts, 'status_choices': Incident.Status.choices, 'category_choices': Incident.Category.choices})


@login_required
@user_passes_test(is_authority)
def manage_incident(request, pk):
    incident = get_object_or_404(Incident, pk=pk)
    if request.method == 'POST':
        old_status = incident.status
        form = AdminIncidentForm(request.POST, instance=incident)
        if form.is_valid():
            incident = form.save()
            if old_status != incident.status or incident.authority_note:
                StatusUpdate.objects.create(incident=incident, status=incident.status, note=incident.authority_note, updated_by=request.user)
            messages.success(request, 'Incident updated successfully.')
            return redirect('authority_dashboard')
    else:
        form = AdminIncidentForm(instance=incident)
    return render(request, 'incidents/manage.html', {'form': form, 'incident': incident})


def incidents_api(request):
    data = []
    qs = Incident.objects.filter(is_public=True).exclude(status=Incident.Status.REJECTED)
    for i in qs:
        if i.latitude and i.longitude:
            data.append({'title': i.title, 'category': i.get_category_display(), 'status': i.get_status_display(), 'severity': i.get_severity_display(), 'lat': float(i.latitude), 'lng': float(i.longitude), 'location': i.location_name})
    return JsonResponse({'incidents': data})
