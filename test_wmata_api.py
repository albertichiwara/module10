"""This module contains unit tests to verify the functionality of 
the wmata_api endpoint."""

from wmata_api import app
import json
import unittest

class WMATATest(unittest.TestCase):
    """
    Class for unit testing of wmata_api endpoint.
    
    """
    
    def test_http_success(self):
        """Test to ensure both endpoints return a 200 HTTP code."""

         # assert that the response code of 'incidents/escalators returns a 200 code
        escalator_response = app.test_client().get('/incidents/escalators').status_code
        escalator_result = escalator_response / 100
        self.assertGreaterEqual(escalator_result, 2)
        self.assertLess(escalator_result, 3)

       
        # assert that the response code of 'incidents/elevators returns a 200 code
        elevator_response = app.test_client().get('/incidents/elevators').status_code
        elevator_result = elevator_response / 100
        self.assertGreaterEqual(elevator_result, 2)
        self.assertLess(elevator_result, 3)        
        

################################################################################

    
    def test_required_fields(self):
        """Test to ensure all returned incidents have the 4 required fields."""
        required_fields = ["StationCode", "StationName", "UnitType", "UnitName"]

        response = app.test_client().get('/incidents/escalators')
        json_response = json.loads(response.data.decode())
        for incident in json_response:
            for field in required_fields:
                self.assertIn(field, list(incident.keys()))

        elevator_response = app.test_client().get('/incidents/elevators')
        json_elevator_response = json.loads(elevator_response.data.decode())
        for  elevator_incident in json_elevator_response:
            for field in required_fields:
                self.assertIn(field, list(elevator_incident.keys()))

        # for each incident in the JSON response assert that each of the required fields
        # are present in the response

################################################################################

    
    def test_escalators(self):
        """Test to ensure all entries returned by the /escalators endpoint 
        have the "ESCALATOR" UnitType."""
        response = app.test_client().get('/incidents/escalators')
        json_response = json.loads(response.data.decode())
        for incident in json_response:
            self.assertEqual("ESCALATOR", incident['UnitType'])


        # for each incident in the JSON response, assert that the 'UnitType' is "ESCALATOR"

################################################################################

    
    def test_elevators(self):
        """Test to ensure all entries returned by the /elevators endpoint have the "ELEVATOR" UnitType."""
        response = app.test_client().get('/incidents/elevators')
        json_response = json.loads(response.data.decode())
        for incident in json_response:
            self.assertEqual("ELEVATOR", incident['UnitType'])
        # for each incident in the JSON response, assert that the 'UnitType' is "ELEVATOR"

################################################################################

if __name__ == "__main__":
    unittest.main()
   