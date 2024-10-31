"""This module implements a simple web app that gets station incident
information from the mod10 API and allows users to request incidents by 
unit type- escalator or elevator."""

import json
import requests
from flask import Flask, Response

INCIDENTS_URL = "https://jhu-intropython-mod10.replit.app/"


################################################################################

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    """Get incidents by machine type (elevators/escalators)."""

    # create an empty list called 'incidents'
    incidents = []
    # Do a GET request to the mod10 API and get JSON retrieve the JSON from the response
    try:
        response = requests.get(INCIDENTS_URL)
        response.raise_for_status()  # Raise an error if request fails
        response_dict = response.json()
    except requests.RequestException as e:
        error_response = json.dumps({"error": str(e)})
        return Response(error_response, status=500, content_type='application/json')

    elev_incidents = response_dict.get("ElevatorIncidents", [])

    # iterate through the JSON response and retrieve all incidents matching 'unit_type'
    # for each incident, create a dictionary containing StationCode, StationName, UnitType, UnitName
    for e in elev_incidents:
        if e['UnitType'].lower() == unit_type.lower():
            # add each incident dictionary object to the 'incidents' list
            incidents.append({'StationCode': e['StationCode'], 'StationName': e['StationName']
                              , 'UnitName': e['UnitName'], 'UnitType': e['UnitType']})

    # return a list of incident dictionaries using json.dumps()
    json_incidents = json.dumps(incidents)

    # Return JSON response
    return Response(json_incidents, content_type='application/json')


if __name__ == '__main__':
    app.run(debug=True)
