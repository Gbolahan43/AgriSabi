import os
import time
import requests

ISDASOIL_USERNAME = os.getenv("ISDASOIL_USERNAME")
ISDASOIL_PASSWORD = os.getenv("ISDASOIL_PASSWORD")
BASE_URL = "https://api.isda-africa.com"

_access_token = None
_token_expiry = 0

def get_isdasoil_token():
    """Authenticate and fetch a rolling 60-minute JWT token from iSDAsoil."""
    global _access_token, _token_expiry
    
    # Use cached token if it is valid for at least 1 more minute
    if _access_token and time.time() < (_token_expiry - 60):
        return _access_token
        
    if not ISDASOIL_USERNAME or not ISDASOIL_PASSWORD:
        return None
        
    try:
        response = requests.post(
            f"{BASE_URL}/login", 
            data={"username": ISDASOIL_USERNAME, "password": ISDASOIL_PASSWORD},
            timeout=10
        )
        if response.status_code == 200:
            _access_token = response.json().get("access_token")
            _token_expiry = time.time() + 3600  # API tokens expire in 60 minutes
            return _access_token
        else:
            print(f"iSDAsoil Auth Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"iSDAsoil Connection Error: {e}")
        return None

def get_soil_data(latitude: float, longitude: float) -> str:
    """
    Native Tool for Advisory Agent: Fetches soil parameters (pH) for an exact lat/lon coordinate.
    """
    token = get_isdasoil_token()
    if not token:
        return "Soil data is currently unavailable. Authentication failed or credentials missing."
        
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Fetching topsoil pH (0-20cm depth)
        url = f"{BASE_URL}/isdasoil/v2/soilproperty?lat={latitude}&lon={longitude}&property=ph&depth=0-20"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            try:
                ph_value = data['property']['ph'][0]['value']['value']
                return f"Detailed Topsoil Check (0-20cm) at [{latitude}, {longitude}]: The pH level is {ph_value}."
            except KeyError:
                return f"Could not parse soil pH from the African soil database for [{latitude}, {longitude}]."
        else:
            return f"Failed to retrieve soil data. Server responded with {response.status_code}."
            
    except Exception as e:
        print(f"iSDAsoil Request Error: {e}")
        return "Encountered a network error while fetching soil data."
