from flask import Blueprint, request, jsonify

location_api = Blueprint('location_api', __name__)

# Mock data for countries and cities
COUNTRIES = [
    {"place_id": "IL", "name": "Israel", "host_count": 15},
    {"place_id": "USA", "name": "United States", "host_count": 8},
    {"place_id": "BR", "name": "Brazil", "host_count": 3},
    {"place_id": "FC", "name": "France", "host_count": 5}
]

CITIES = [
    {"place_id": "IL-JM", "name": "Jerusalem", "country_place_id": "IL"},
    {"place_id": "IL-TA", "name": "Tel Aviv", "country_place_id": "IL"},
    {"place_id": "IL-HF", "name": "Haifa", "country_place_id": "IL"},
    {"place_id": "USA-NY", "name": "New York", "country_place_id": "USA"},
    {"place_id": "USA-LA", "name": "Los Angeles", "country_place_id": "USA"},
    {"place_id": "BR-SP", "name": "São Paulo", "country_place_id": "BR"},
    {"place_id": "FC-PA", "name": "Paris", "country_place_id": "FC"}
]


@location_api.route("/locations/countries", methods=["GET"])
def get_countries():
    """Get all countries"""
    try:
        print(f"DEBUG: Returning {len(COUNTRIES)} countries: {COUNTRIES}")
        return jsonify(COUNTRIES)
    except Exception as e:
        print(f"ERROR: Failed to fetch countries: {e}")
        return jsonify({"error": "Failed to fetch countries"}), 500


@location_api.route("/locations/cities/country/<country_place_id>", methods=["GET"])
def get_cities_by_country(country_place_id):
    """Get cities by country"""
    try:
        cities = [city for city in CITIES if city["country_place_id"] == country_place_id]
        return jsonify(cities)
    except Exception as e:
        return jsonify({"error": "Failed to fetch cities"}), 500


@location_api.route("/locations/search", methods=["GET"])
def search_locations():
    """Search locations"""
    try:
        query = request.args.get("query", "").lower()
        country_place_id = request.args.get("country_place_id")
        city_place_id = request.args.get("city_place_id")
        limit = int(request.args.get("limit", 10))
        
        # Filter countries
        countries = []
        if query:
            countries = [c for c in COUNTRIES if query in c["name"].lower()]
        elif country_place_id:
            countries = [c for c in COUNTRIES if c["place_id"] == country_place_id]
        else:
            countries = COUNTRIES[:limit//2]
        
        # Filter cities
        cities = []
        if query:
            cities = [c for c in CITIES if query in c["name"].lower()]
        elif country_place_id:
            cities = [c for c in CITIES if c["country_place_id"] == country_place_id]
        elif city_place_id:
            cities = [c for c in CITIES if c["place_id"] == city_place_id]
        else:
            cities = CITIES[:limit//2]
        
        return jsonify({
            "countries": countries[:limit//2],
            "cities": cities[:limit//2]
        })
    except Exception as e:
        return jsonify({"error": "Failed to search locations"}), 500


@location_api.route("/locations/reverse-geocode", methods=["GET"])
def reverse_geocode():
    """Get location by coordinates"""
    try:
        lat = request.args.get("lat")
        lng = request.args.get("lng")
        
        # Mock response - in real implementation, you would use Google Maps API
        return jsonify({
            "country_place_id": "IL",
            "city_place_id": "IL-JM",
            "address": "Jerusalem, Israel"
        })
    except Exception as e:
        return jsonify({"error": "Failed to get location by coordinates"}), 500


@location_api.route("/locations/nearby", methods=["GET"])
def get_nearby_locations():
    """Get nearby locations"""
    try:
        lat = request.args.get("lat")
        lng = request.args.get("lng")
        radius = request.args.get("radius", 10)
        
        # Mock response
        return jsonify({
            "countries": COUNTRIES[:2],
            "cities": CITIES[:3]
        })
    except Exception as e:
        return jsonify({"error": "Failed to get nearby locations"}), 500


@location_api.route("/locations/popular", methods=["GET"])
def get_popular_locations():
    """Get popular locations"""
    try:
        return jsonify({
            "countries": COUNTRIES[:3],
            "cities": CITIES[:5]
        })
    except Exception as e:
        return jsonify({"error": "Failed to get popular locations"}), 500


@location_api.route("/locations/autocomplete", methods=["GET"])
def get_location_autocomplete():
    """Get location autocomplete suggestions"""
    try:
        query = request.args.get("query", "").lower()
        
        if not query:
            return jsonify([])
        
        # Search in countries and cities
        results = []
        
        # Add countries
        for country in COUNTRIES:
            if query in country["name"].lower():
                results.append({
                    "place_id": country["place_id"],
                    "description": f"{country['name']} (Country)"
                })
        
        # Add cities
        for city in CITIES:
            if query in city["name"].lower():
                country_name = next((c["name"] for c in COUNTRIES if c["place_id"] == city["country_place_id"]), "")
                results.append({
                    "place_id": city["place_id"],
                    "description": f"{city['name']}, {country_name}"
                })
        
        return jsonify(results[:10])  # Limit to 10 results
    except Exception as e:
        return jsonify({"error": "Failed to get autocomplete suggestions"}), 500
