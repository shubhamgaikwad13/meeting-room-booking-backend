import json

class Employee:
    __tablename__: 'Employee'

    def __init__(self, id, first_name, last_name, email, phone, designation, is_active, is_admin):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.designation = designation
        self.is_active = is_active
        self.is_admin = is_admin
        print("constructor")


    @staticmethod
    def get_employees(employees):
        data = []
        for emp in employees:
            emp_dict = {
                '_id': emp[0],
                'first_name': emp[1],
                'last_name': emp[2],
                'email': emp[3],
                'password': emp[4],
                'phone': emp[5],
                'designation': emp[6],
                'is_admin': emp[7]
            }
            data.append(emp_dict)
        return json.dumps(data)

    def demo():
        pass



