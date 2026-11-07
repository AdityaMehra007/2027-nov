"""==============================================================================
AETHER SATELLITE GEOSPATIAL VIEWER & INUNDATION MAP TEMPLATE
==============================================================================
Interactive WebGL/Leaflet WGS84 hazard visualization overlay for Sentinel-1
SAR backscatter flood masks, critical infrastructure, and resilience routing.
==============================================================================
"""

from typing import List, Dict, Any, Optional
import json

def get_default_sar_flood_zones() -> List[Dict[str, Any]]:
    """Returns curated Sentinel-1 SAR flood risk zones with WGS84 polygons."""
    return [
        {
            "name": "Bellandur Basin & ORR Tech Corridor",
            "zone_id": "SAR-BLR-01",
            "risk_level": "CRITICAL",
            "inundation_area_km2": 4.82,
            "otsu_threshold_db": -16.4,
            "vulnerability_index": 88.5,
            "coordinates": [
                [12.9360, 77.6620],
                [12.9420, 77.6780],
                [12.9290, 77.6850],
                [12.9220, 77.6680],
                [12.9360, 77.6620]
            ],
            "critical_infra": ["Ecospace Tech Park", "Substation 66kV", "ORR Arterial Road"]
        },
        {
            "name": "Varthur Wetland & Spillway Buffer",
            "zone_id": "SAR-BLR-02",
            "risk_level": "HIGH",
            "inundation_area_km2": 3.45,
            "otsu_threshold_db": -17.1,
            "vulnerability_index": 79.0,
            "coordinates": [
                [12.9520, 77.7050],
                [12.9600, 77.7220],
                [12.9460, 77.7340],
                [12.9380, 77.7120],
                [12.9520, 77.7050]
            ],
            "critical_infra": ["Whitefield Link Road", "Primary Water Pipeline", "Residential Enclaves"]
        },
        {
            "name": "Rainbow Drive / Sarjapur Depression",
            "zone_id": "SAR-BLR-03",
            "risk_level": "HIGH",
            "inundation_area_km2": 1.95,
            "otsu_threshold_db": -16.8,
            "vulnerability_index": 74.2,
            "coordinates": [
                [12.9100, 77.6900],
                [12.9180, 77.7010],
                [12.9120, 77.7080],
                [12.9030, 77.6970],
                [12.9100, 77.6900]
            ],
            "critical_infra": ["Sarjapur Main Road", "Feeder Power Transformers"]
        },
        {
            "name": "Manyata Tech Basin / Hebbal Valley",
            "zone_id": "SAR-BLR-04",
            "risk_level": "MEDIUM",
            "inundation_area_km2": 2.60,
            "otsu_threshold_db": -15.9,
            "vulnerability_index": 58.0,
            "coordinates": [
                [13.0450, 77.6150],
                [13.0550, 77.6280],
                [13.0480, 77.6390],
                [13.0370, 77.6250],
                [13.0450, 77.6150]
            ],
            "critical_infra": ["Hebbal Flyover Ingress", "Nagavara Metro Pillar Line", "Data Center Annex"]
        }
    ]

def render_aether_map_html(
    initial_lat: float = 12.9400,
    initial_lon: float = 77.6800,
    initial_zoom: int = 12,
    zones_data: Optional[List[Dict[str, Any]]] = None
) -> str:
    """Renders high-fidelity Sentinel-1 geospatial inundation map HTML."""
    zones = zones_data if zones_data is not None else get_default_sar_flood_zones()
    zones_json = json.dumps(zones)

    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AETHER // Sentinel-1 SAR Geospatial Inundation Observatory</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #070a12; }}
        .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
        #map {{ height: calc(100vh - 72px); width: 100%; }}
        .leaflet-container {{ background: #070a12 !important; }}
        .hud-glass {{ background: rgba(7, 10, 18, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(6, 182, 212, 0.25); }}
    </style>
</head>
<body class="text-gray-100 h-screen flex flex-col overflow-hidden bg-[#070a12]">
    <!-- Top Nav / Control Bar -->
    <header class="h-[72px] border-b border-gray-800 bg-[#070a12]/95 px-6 flex items-center justify-between z-30">
        <div class="flex items-center space-x-4">
            <div class="w-10 h-10 rounded-xl bg-cyan-950/80 border border-cyan-500/40 flex items-center justify-center text-cyan-400 font-bold text-lg">
                🛰️
            </div>
            <div>
                <h1 class="text-sm md:text-base font-extrabold tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-emerald-400 font-mono">
                    AETHER // GEOSPATIAL SAR OBSERVATORY
                </h1>
                <p class="text-[10px] font-mono text-gray-500 uppercase tracking-widest">
                    Copernicus Sentinel-1 C-Band Backscatter • WGS84 Dynamic Flood Inundation
                </p>
            </div>
        </div>

        <div class="flex items-center space-x-3">
            <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-mono font-bold bg-emerald-950/60 border border-emerald-500/40 text-emerald-300">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping mr-2"></span>
                SAR STREAM LIVE
            </span>
            <a href="/portal" class="px-3 py-1.5 rounded-lg border border-gray-700 hover:border-gray-500 text-xs font-mono text-gray-300 hover:text-white transition">
                Portal
            </a>
            <a href="/api/v1/dashboard" class="px-3 py-1.5 rounded-lg bg-cyan-500 text-black font-extrabold text-xs font-mono hover:bg-cyan-400 transition">
                Dashboard
            </a>
        </div>
    </header>

    <!-- Main Map Workspace -->
    <div class="relative flex-1 flex">
        <!-- Full-bleed Leaflet Container -->
        <div id="map" class="z-10"></div>

        <!-- Floating Left Telemetry HUD -->
        <div class="absolute top-4 left-4 z-20 w-80 hud-glass rounded-2xl p-5 space-y-4 shadow-2xl">
            <div class="flex items-center justify-between border-b border-gray-800 pb-3">
                <span class="text-xs font-mono font-bold uppercase tracking-widest text-cyan-400">Satellite HUD</span>
                <span class="text-[10px] font-mono text-gray-400">VV/VH InSAR</span>
            </div>

            <div class="grid grid-cols-2 gap-3">
                <div class="bg-gray-900/80 p-3 rounded-xl border border-gray-800">
                    <span class="text-[10px] font-mono text-gray-500 uppercase block">Otsu Threshold</span>
                    <span class="text-base font-extrabold text-cyan-300 font-mono">-16.4 dB</span>
                </div>
                <div class="bg-gray-900/80 p-3 rounded-xl border border-gray-800">
                    <span class="text-[10px] font-mono text-gray-500 uppercase block">Inundation</span>
                    <span class="text-base font-extrabold text-emerald-400 font-mono">12.82 km²</span>
                </div>
            </div>

            <div class="space-y-1">
                <span class="text-[10px] font-mono text-gray-400 uppercase tracking-wider block">Target Location Presets:</span>
                <div class="grid grid-cols-2 gap-2 text-xs font-mono">
                    <button onclick="flyToLoc(12.9360, 77.6780, 13)" class="px-2 py-1.5 bg-gray-900 hover:bg-gray-800 rounded border border-gray-700 text-left text-cyan-300">
                        📍 Bellandur ORR
                    </button>
                    <button onclick="flyToLoc(12.9520, 77.7150, 13)" class="px-2 py-1.5 bg-gray-900 hover:bg-gray-800 rounded border border-gray-700 text-left text-cyan-300">
                        📍 Varthur Spill
                    </button>
                    <button onclick="flyToLoc(13.0450, 77.6250, 13)" class="px-2 py-1.5 bg-gray-900 hover:bg-gray-800 rounded border border-gray-700 text-left text-cyan-300">
                        📍 Manyata Basin
                    </button>
                    <button onclick="flyToLoc(12.9100, 77.6970, 13)" class="px-2 py-1.5 bg-gray-900 hover:bg-gray-800 rounded border border-gray-700 text-left text-cyan-300">
                        📍 Sarjapur Plain
                    </button>
                </div>
            </div>

            <div class="pt-2 border-t border-gray-800">
                <span class="text-[10px] font-mono text-gray-400 uppercase block mb-1">Click Map To Evaluate Risk:</span>
                <div id="inspector-output" class="text-xs font-mono text-gray-300 bg-gray-900/90 p-3 rounded-xl border border-gray-800 min-h-[72px] flex items-center justify-center text-center text-gray-500">
                    Click anywhere on the map or select a zone above to calculate localized vulnerability score.
                </div>
            </div>
        </div>

        <!-- Floating Legend Bottom Right -->
        <div class="absolute bottom-6 right-6 z-20 hud-glass rounded-xl p-4 shadow-xl text-xs font-mono space-y-2">
            <span class="font-bold text-gray-300 text-[10px] uppercase tracking-widest block">Hydrological Risk Legend</span>
            <div class="flex items-center space-x-2">
                <span class="w-3 h-3 rounded bg-red-500/80 border border-red-400"></span>
                <span class="text-gray-300">Critical Flood Extent (>80)</span>
            </div>
            <div class="flex items-center space-x-2">
                <span class="w-3 h-3 rounded bg-amber-500/80 border border-amber-400"></span>
                <span class="text-gray-300">High Inundation Basin (70-80)</span>
            </div>
            <div class="flex items-center space-x-2">
                <span class="w-3 h-3 rounded bg-cyan-500/80 border border-cyan-400"></span>
                <span class="text-gray-300">Moderate Retention Zone (<70)</span>
            </div>
        </div>
    </div>

    <script>
        const initialLat = {initial_lat};
        const initialLon = {initial_lon};
        const initialZoom = {initial_zoom};
        const zones = {zones_json};

        // Initialize Leaflet Map with CartoDB Dark Matter tiles
        const map = L.map('map', {{
            center: [initialLat, initialLon],
            zoom: initialZoom,
            zoomControl: false
        }});

        L.control.zoom({{ position: 'bottomleft' }}).addTo(map);

        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
            attribution: '&copy; OpenStreetMap contributors &copy; CARTO &copy; Copernicus Sentinel-1',
            subdomains: 'abcd',
            maxZoom: 19
        }}).addTo(map);

        // Color coding for hazard polygons
        function getRiskColor(risk) {{
            if (risk === 'CRITICAL') return '#ef4444';
            if (risk === 'HIGH') return '#f59e0b';
            return '#06b6d4';
        }}

        // Render GeoJSON polygons
        zones.forEach(zone => {{
            const color = getRiskColor(zone.risk_level);
            const polygon = L.polygon(zone.coordinates, {{
                color: color,
                weight: 2,
                opacity: 0.9,
                fillColor: color,
                fillOpacity: 0.35
            }}).addTo(map);

            const popupHtml = `
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #111;">
                    <strong style="font-size: 13px; color: #000;">${{zone.name}}</strong><br>
                    <strong>ID:</strong> ${{zone.zone_id}} | <strong>Risk:</strong> ${{zone.risk_level}}<br>
                    <strong>Vulnerability:</strong> ${{zone.vulnerability_index}} / 100<br>
                    <strong>Inundation Area:</strong> ${{zone.inundation_area_km2}} km²<br>
                    <strong>SAR Otsu dB:</strong> ${{zone.otsu_threshold_db}} dB<br>
                    <hr style="margin: 6px 0; border: none; border-top: 1px solid #ccc;">
                    <strong>Critical Assets:</strong><br>
                    ${{zone.critical_infra.map(i => "• " + i).join("<br>")}}
                </div>
            `;
            polygon.bindPopup(popupHtml);

            polygon.on('click', () => {{
                document.getElementById('inspector-output').innerHTML = `
                    <div class="text-left space-y-1 w-full">
                        <div class="text-cyan-400 font-bold">${{zone.name}}</div>
                        <div class="text-gray-300">Vulnerability: <span class="text-amber-400 font-bold">${{zone.vulnerability_index}}</span> / 100</div>
                        <div class="text-gray-400 text-[10px]">SAR Inundation: ${{zone.inundation_area_km2}} km² (${{zone.otsu_threshold_db}} dB)</div>
                        <div class="text-emerald-400 text-[10px] mt-1">Status: Gated under RentShield escrow.</div>
                    </div>
                `;
            }});
        }});

        function flyToLoc(lat, lon, zoom) {{
            map.flyTo([lat, lon], zoom, {{ duration: 1.2 }});
        }}

        // Map Click Inspector
        map.on('click', async function(e) {{
            const lat = e.latlng.lat.toFixed(4);
            const lon = e.latlng.lng.toFixed(4);

            document.getElementById('inspector-output').innerHTML = `
                <div class="text-left space-y-1 w-full">
                    <div class="text-cyan-400 font-bold">📍 Coordinate Picked</div>
                    <div class="text-gray-300">WGS84: ${{lat}}° N, ${{lon}}° E</div>
                    <div class="text-emerald-400 text-[10px]">Evaluating Aether hydrology model...</div>
                </div>
            `;

            try {{
                const res = await fetch('/api/v1/aether/evaluate', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ lat: parseFloat(lat), lon: parseFloat(lon), hazard: 'FLOOD' }})
                }});
                if (res.ok) {{
                    const data = await res.json();
                    document.getElementById('inspector-output').innerHTML = `
                        <div class="text-left space-y-1 w-full">
                            <div class="text-cyan-400 font-bold">Risk Assessment: <span class="${{data.risk_level === 'CRITICAL' ? 'text-red-400' : (data.risk_level === 'HIGH' ? 'text-amber-400' : 'text-emerald-400')}}">${{data.risk_level}}</span></div>
                            <div class="text-gray-300 text-[11px]">Vulnerability Score: <strong>${{data.vulnerability_index.toFixed(1)}}</strong> / 100</div>
                            <div class="text-gray-400 text-[10px]">Nearby Assets: ${{data.critical_infrastructure_nearby.slice(0, 2).join(', ') || 'Rural Plain'}}</div>
                        </div>
                    `;
                }}
            }} catch(err) {{
                // Handled gracefully in UI
            }}
        }});
    </script>
</body>
</html>
"""
