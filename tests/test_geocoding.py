import unittest
from unittest.mock import patch
import pandas as pd
from pyloghub.geocoding import forward_geocoding  # Replace 'your_module' with the actual name of your module

class TestForwardGeocoding(unittest.TestCase):
    def setUp(self):
        # Sample input data
        self.data = {
            'country': ['DE', 'DE'],
            'state': ['BW', 'BW'],
            'postalCode': ['69117', '69123'],
            'city': ['Heidelberg', 'Heidelberg'],
            'street': ['Schlosshof 1', 'Wieblinger Weg 94']
        }
        self.addresses_df = pd.DataFrame(self.data)

        # Sample output data
        self.expected_output = pd.DataFrame(
            [
                {
                    "country": "DE",
                    "state": "BW",
                    "postalCode": "69117",
                    "city": "Heidelberg",
                    "street": "Schlosshof 1",
                    "parsedCountry": "DE",
                    "parsedState": "Baden-Württemberg",
                    "parsedPostalCode": "69117",
                    "parsedCity": "Heidelberg",
                    "parsedStreet": " 1",
                    "parsedLatitude": 49.4103591,
                    "parsedLongitude": 8.7157387,
                    "validationQuality": 81
                },
                {
                    "country": "DE",
                    "state": "BW",
                    "postalCode": "69123",
                    "city": "Heidelberg",
                    "street": "Wieblinger Weg 94",
                    "parsedCountry": "DE",
                    "parsedState": "Baden-Württemberg",
                    "parsedPostalCode": "69123",
                    "parsedCity": "Heidelberg",
                    "parsedStreet": "Wieblinger Weg 94 ",
                    "parsedLatitude": 49.411858,
                    "parsedLongitude": 8.6477021,
                    "validationQuality": 86
                }
            ]
        )

    @patch('log_hub.geocoding.requests.post')
    def test_forward_geocoding(self, mock_post):
        # Mocking the API response
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "geocodes": self.expected_output.to_dict(orient='records')
        }

        # Call the function
        result = forward_geocoding(self.addresses_df, 'dummy_api_key')

        # Check if the result matches the expected output
        pd.testing.assert_frame_equal(result, self.expected_output)

if __name__ == '__main__':
    unittest.main()

