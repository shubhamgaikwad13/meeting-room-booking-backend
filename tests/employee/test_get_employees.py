import unittest
import requests
from http import HTTPStatus

class GetEmployees(unittest.TestCase):
    BASE_URI = "http://127.0.0.1:5001/"

    credentials = {
        "email" : "subham.gaikwad@opcito.com",
        "password" : "Opcito@123"
    }
    # function for login, it will be called first whenever this class is used
    def setUp(self):
        response = requests.post(self.BASE_URI + "auth/" , json=self.credentials)
        # print(response.cookies.get('access_token_cookie'))
        self.token = response.cookies.get('access_token_cookie')

    # test for success response for get employee
    def test_get_employees(self):        
        response = requests.get(self.BASE_URI + "employee/", cookies={'access_token_cookie': self.token})
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # test for unsuccessful login
    def test_get_employee_without_login(self):
        response = requests.get(self.BASE_URI + "employee/")
        # print(response.__dict__["_content"])
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.json()["msg"], "Missing cookie \"access_token_cookie\"")

     # function for logout, it will be called last whenever this class is used
    def tearDown(self):
        response = requests.post(self.BASE_URI + "auth/logout")

if(__name__)=="__main__":
    unittest.main()