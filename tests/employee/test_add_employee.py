import unittest
import requests
from http import HTTPStatus

class GetEmployees(unittest.TestCase):
    BASE_URI = "http://127.0.0.1:5001/"

    credentials = {
        "email" : "yash.gaykar@gmail.com",
        "password" : "Opcito@123"
    }

    basic_data = {
        "_id" : "OPI004",
        "first_name" : "Subham",
        "last_name" : "Gaikawad",
        "email" : "subham.gaikwad@gmail.com",
        "password" : "Opcito@123",
        "phone" : "9087654390",
        "designation" : "Trainee",
        "is_admin" : False,
        "created_by" : "OPI001"
    }

    # function for login, it will be called first whenever this class is used
    def setUp(self):
        response = requests.post(self.BASE_URI + "auth/" , json=self.credentials)
        # print(response.cookies.get('access_token_cookie'))
        self.token = response.cookies.get('access_token_cookie')

    # def test_successful_employee_addition(self):
    #     response = requests.post(self.BASE_URI + "employee/", json=)

     # function for logout, it will be called last whenever this class is used
    def tearDown(self):
        response = requests.post(self.BASE_URI + "auth/logout")

if(__name__)=="__main__":
    unittest.main()