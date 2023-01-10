import requests
 
def test_get_employees():
    response = requests.get("http://127.0.0.1:5001/employee/")
    print("response",response.json())
    # return respons

test_get_employees()