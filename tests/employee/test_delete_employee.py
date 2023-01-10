import unittest
import requests
from http import HTTPStatus

class GetEmployees(unittest.TestCase):
    BASE_URI = "http://127.0.0.1:5001/"

    credentials = {
        "email" : "yash.gaykar@gmail.com",
        "password" : "Opcito@123"
    }
    required_data = {"updated_by" : "OPI001"}
    # function for login, it will be called first whenever this class is used
    def setUp(self):
        response = requests.post(self.BASE_URI + "auth/" , json=self.credentials)
        # print(response.cookies.get('access_token_cookie'))
        self.token = response.cookies.get('access_token_cookie')

    # test for successful deletion of employee
    def test_successful_employee_deletion(self):
        response = requests.delete(
            self.BASE_URI + "/employee/OPI004",
            cookies = {'access_token_cookie': self.token},
            json = self.required_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()["message"], "Employee deleted successfully.")

     # function for logout, it will be called last whenever this class is used
    def tearDown(self):
        response = requests.post(self.BASE_URI + "auth/logout")

if(__name__)=="__main__":
    unittest.main()