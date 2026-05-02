document.addEventListener('DOMContentLoaded', () => {
  const mapEl = document.getElementById('map');
  if (!mapEl || !window.L) return;

  const isReportPage = Boolean(document.getElementById('incident-form'));
  const map = L.map('map', {
    zoomControl: true,
    scrollWheelZoom: true,
    doubleClickZoom: true
  }).setView([33.5333, -5.1067], 12);

  // CartoDB tiles avoid the OpenStreetMap 403/referrer issue seen on localhost.
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 20,
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
  }).addTo(map);

  const colors = {
    fire: '#f97316',
    logging: '#16a34a',
    water_leak: '#0284c7',
    pollution: '#7c3aed',
    drought: '#eab308',
    wildlife: '#22c55e',
    other: '#64748b'
  };

  const icons = {
    fire: '🔥',
    logging: '🌲',
    water_leak: '💧',
    pollution: '☣️',
    drought: '☀️',
    wildlife: '🦌',
    other: '📍'
  };

  function categoryKey(categoryText) {
    const text = String(categoryText || '').toLowerCase();
    if (text.includes('fire') || text.includes('smoke')) return 'fire';
    if (text.includes('water') || text.includes('leak')) return 'water_leak';
    if (text.includes('drought') || text.includes('scarcity')) return 'drought';
    if (text.includes('pollution') || text.includes('waste')) return 'pollution';
    if (text.includes('wildlife') || text.includes('ecosystem')) return 'wildlife';
    if (text.includes('logging') || text.includes('forest')) return 'logging';
    return 'other';
  }

  function addIncidentCircle(lat, lng, categoryText, severityText) {
    const key = categoryKey(categoryText);
    const color = colors[key];
    const severity = String(severityText || '').toLowerCase();
    const radius = severity.includes('critical') ? 380 : severity.includes('high') ? 300 : 220;

    L.circle([lat, lng], {
      color,
      fillColor: color,
      fillOpacity: 0.32,
      weight: 3,
      radius
    }).addTo(map);

    L.marker([lat, lng], {
      icon: L.divIcon({
        className: 'incident-map-icon',
        html: `<div class="map-emoji" style="border-color:${color}">${icons[key]}</div>`,
        iconSize: [40, 40],
        iconAnchor: [20, 20]
      }),
      interactive: false
    }).addTo(map);
  }

  if (isReportPage) {
    let selected = false;
    let marker = null;
    const latInput = document.getElementById('id_latitude');
    const lngInput = document.getElementById('id_longitude');
    const selectedMessage = document.getElementById('map-selected');

    function setSelectedLocation(lat, lng, zoom = 15) {
      selected = true;
      if (marker) map.removeLayer(marker);
      marker = L.marker([lat, lng], {
        icon: L.divIcon({
          className: 'selected-location-icon',
          html: '<div class="selected-pin"><i class="fa-solid fa-location-dot"></i></div>',
          iconSize: [46, 46],
          iconAnchor: [23, 42]
        })
      }).addTo(map);
      latInput.value = lat.toFixed(6);
      lngInput.value = lng.toFixed(6);
      map.setView([lat, lng], zoom);
      if (selectedMessage) selectedMessage.classList.remove('hidden');
    }

    map.on('click', (e) => setSelectedLocation(e.latlng.lat, e.latlng.lng, map.getZoom()));

    const geoBtn = document.getElementById('use-location');
    if (geoBtn) {
      geoBtn.addEventListener('click', () => {
        if (!navigator.geolocation) {
          alert('Geolocation is not available in this browser. Please click the map instead.');
          return;
        }
        geoBtn.disabled = true;
        geoBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Locating...';
        navigator.geolocation.getCurrentPosition(
          (pos) => {
            setSelectedLocation(pos.coords.latitude, pos.coords.longitude, 16);
            geoBtn.disabled = false;
            geoBtn.innerHTML = '<i class="fa-solid fa-location-crosshairs"></i> Use my location';
          },
          () => {
            alert('Could not access your location. Please click the map manually.');
            geoBtn.disabled = false;
            geoBtn.innerHTML = '<i class="fa-solid fa-location-crosshairs"></i> Use my location';
          },
          { enableHighAccuracy: true, timeout: 8000 }
        );
      });
    }

    const form = document.getElementById('incident-form');
    if (form) {
      form.addEventListener('submit', (e) => {
        if (!selected || !latInput.value || !lngInput.value) {
          e.preventDefault();
          alert('Please select the incident location on the map before submitting.');
          mapEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      });
    }
  } else {
    fetch('/api/incidents/')
      .then((r) => r.json())
      .then((data) => {
        const points = [];
        data.incidents.forEach((incident) => {
          const lat = Number(incident.lat);
          const lng = Number(incident.lng);
          if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;
          addIncidentCircle(lat, lng, incident.category, incident.severity);
          points.push([lat, lng]);
        });
        if (points.length) map.fitBounds(points, { padding: [30, 30], maxZoom: 14 });
      })
      .catch(() => {});
  }
});
