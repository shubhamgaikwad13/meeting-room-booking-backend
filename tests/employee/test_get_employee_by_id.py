import unittest
import requests
from http import HTTPStatus

class GetEmployeeById(unittest.TestCase):
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

    # test for success response for get employee by id
    def test_successful_get_employees_by_id(self):        
        response = requests.get(self.BASE_URI + "employee/OPI001", cookies={'access_token_cookie': self.token})
        id = response.json()["employee"]["_id"]
        self.assertEqual(id, "OPI001")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # test for unsuccessful get request
    def test_get_employee_without_id(self):
        response = requests.get(self.BASE_URI + "employee/fjksdbfksd", cookies={'access_token_cookie': self.token})
        # print("res: ", response.json()["message"])
        self.assertEqual(response.json()["message"], "Employee not found.")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

     # function for logout, it will be called last whenever this class is used
    def tearDown(self):
        response = requests.post(self.BASE_URI + "auth/logout")

if(__name__)=="__main__":
    unittest.main()