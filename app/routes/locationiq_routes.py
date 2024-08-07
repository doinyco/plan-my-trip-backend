from flask import Blueprint, jsonify, request
import requests
import os

# This route is for using the LocationIQ API instead of the frontend due to key security
bp = Blueprint('locationiq', __name__, url_prefix="/locationiq")

@bp.get("")
def get_locations():
    api_key = os.getenv("LOCATIONIQ_API_KEY")
    query = request.args.get('q')
    params = {
        "key": api_key,
        "q": query,
        "format": "json",
        "limit": 5,
        "dedupe": 1,
        "tag": "place:*"
    }

    response = requests.get("https://api.locationiq.com/v1/autocomplete", params=params)
    return jsonify(response.json()), response.status_code
