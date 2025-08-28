from flask import Blueprint, jsonify
from locations.country_service import CountryService

country_api = Blueprint("country_api", __name__, url_prefix="/api/countries")

@country_api.get("/locations/countries")
def top_hosts_per_country():
    svc = CountryService()
    data = svc.get_top5_hosts_per_country()
    return jsonify(data), 200