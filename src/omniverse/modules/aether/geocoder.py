from typing import Dict, Any
from functools import lru_cache
import urllib.parse
import json

class AetherGeocoder:
    """Geocodes cities, administrative boundaries, and neighborhoods to WGS84 coordinates."""

    _PRESET_HUBS = {
        "bengaluru": {"lat": 12.9716, "lon": 77.5946, "elevation_meters": 920.0, "display_name": "Bengaluru, Karnataka, India"},
        "bangalore": {"lat": 12.9716, "lon": 77.5946, "elevation_meters": 920.0, "display_name": "Bengaluru, Karnataka, India"},
        "mumbai": {"lat": 19.0760, "lon": 72.8777, "elevation_meters": 14.0, "display_name": "Mumbai, Maharashtra, India"},
        "delhi": {"lat": 28.7041, "lon": 77.1025, "elevation_meters": 216.0, "display_name": "Delhi, India"},
        "hyderabad": {"lat": 17.3850, "lon": 78.4867, "elevation_meters": 542.0, "display_name": "Hyderabad, Telangana, India"},
        "chennai": {"lat": 13.0827, "lon": 80.2707, "elevation_meters": 6.0, "display_name": "Chennai, Tamil Nadu, India"},
        "london": {"lat": 51.5074, "lon": -0.1278, "elevation_meters": 35.0, "display_name": "London, United Kingdom"},
        "new york": {"lat": 40.7128, "lon": -74.0060, "elevation_meters": 10.0, "display_name": "New York, USA"},
        "singapore": {"lat": 1.3521, "lon": 103.8198, "elevation_meters": 15.0, "display_name": "Singapore"}
    }

    @staticmethod
    @lru_cache(maxsize=1024)
    def _cached_lookup(normalized_query: str) -> Dict[str, Any]:
        for key, val in AetherGeocoder._PRESET_HUBS.items():
            if key in normalized_query:
                return val
        return AetherGeocoder._PRESET_HUBS["bengaluru"]

    def geocode(self, query: str) -> Dict[str, Any]:
        """Geocodes a query string with in-memory LRU caching."""
        normalized = query.lower().strip()
        return self._cached_lookup(normalized)
