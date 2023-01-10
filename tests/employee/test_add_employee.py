import unittest
import requests
from http import HTTPStatus

class AddEmployees(unittest.TestCase):
    BASE_URI = "http://127.0.0.1:5001/"

    credentials = {
        "email" : "yash.gaykar@gmail.com",
        "password" : "Opcito@123"
    }


    # function for login, it will be called first whenever this class is used
    def setUp(self):
        response = requests.post(self.BASE_URI + "auth/" , json=self.credentials)
        # print(response.cookies.get('access_token_cookie'))
        self.token = response.cookies.get('access_token_cookie')
        self.csrf = response.cookies.get('csrf_access_token')
        self.basic_data = {
        "_id" : "OPI004",
        "first_name" : "Tushar",
        "last_name" : "Ahire",
        "email" : "tushar.ahire@opcito.com",
        "password" : "Opcito@123",
        "phone" : "7564024284",
        "designation" : "Trainee",
        "is_admin" : False,
        "created_by" : "OPI001"
        }
        # print("----token---", self.csrf)

    # test for successful creation for an employee
    def test_successful_employee_addition(self):
        response = requests.post(
            self.BASE_URI + "employee/",
            cookies={"access_token_cookie" : self.token},
            headers={"X-CSRF-TOKEN" : self.csrf},
            json=self.basic_data)
        print("res", response.json())
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()["message"], "Employee added successfully.")

    # test for addition of employee having one or more duplicate fields(Negative test)
    # def test_duplicate_employee_addition(self):
    #     response = requests.post(
    #         self.BASE_URI + "employee/",
    #         cookies={"access_token_cookie" : self.token},
    #         headers={"X-CSRF-TOKEN" : self.csrf},
    #         json=self.basic_data)
    #     self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    #     self.assertEqual(response.json()["error"], "Duplicate entry for employee PRIMARY.")

    # Test for addition of employee from a non-admin(Negative Test)
    def test_employee_addition_from_non_admin(self):
        self.basic_data["created_by"] = "OPI003"
        response = requests.post(
            self.BASE_URI + "employee/",
            cookies={"access_token_cookie" : self.token},
            headers={"X-CSRF-TOKEN" : self.csrf},
            json=self.basic_data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()["error"], "Only admin can add the user.")

    # test for any key missing in employee schema
    def test_missing_key_in_employee_schema(self):
        del self.basic_data["email"]
        response = requests.post(
            self.BASE_URI + "employee/",
            cookies={"access_token_cookie" : self.token},
            headers={"X-CSRF-TOKEN" : self.csrf},
            json=self.basic_data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()["error"], "email is required.")

    # test for employee addition where expected type of a key is different
    def test_worng_type_input(self):
        self.basic_data["_id"] = 1
        response = requests.post(
            self.BASE_URI + "employee/",
            cookies={"access_token_cookie" : self.token},
            headers={"X-CSRF-TOKEN" : self.csrf},
            json=self.basic_data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json()["error"], "_id must be of type <class 'str'>")

     # function for logout, it will be called last whenever this class is used
    def tearDown(self):
        response = requests.post(self.BASE_URI + "auth/logout")

if(__name__)=="__main__":
    unittest.main()

