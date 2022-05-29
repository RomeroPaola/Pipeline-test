import unittest
import requests

class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000/api/team"


    def test_get_all_teams(self):
        response = requests.get(self.URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 18)
        print("Test 1 completed") 

if __name__ == "__main__":
    tester = TestAPI()

    tester.test_get_all_teams()         