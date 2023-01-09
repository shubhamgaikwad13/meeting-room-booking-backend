from flask import g, jsonify
from ...utils import make_response
from .constant import *
from werkzeug.security import generate_password_hash


class Employee:
    __tablename__: 'Employee'

    def __init__(self, _id, first_name, last_name, email, password, phone, designation, is_active=True, is_admin=False, created_by=None):
        self._id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.phone = phone
        self.designation = designation
        self.is_active = is_active
        self.is_admin = is_admin
        self.created_by = created_by

    @staticmethod
    def get_employees():
        """Fetches all employees from the database

        Returns:
            list: List of employees with each employee as a dictionary
        """
        cursor = g.db.cursor(dictionary=True)
        query = '''SELECT _id, first_name, last_name, email, phone, designation, is_admin FROM Employee WHERE is_active=true'''
        cursor.execute(query)
        employees = cursor.fetchall()

        return employees

    @staticmethod
    def get_employee_by_id(employee_id):
        """Fetches employee by id if employee is active

        Returns:
            object: Employee 
        """

        cursor = g.db.cursor()

        query = '''SELECT * FROM Employee WHERE _id = %(_id)s AND is_active=true'''
        params = {'_id': employee_id}
        cursor.execute(query, params)
        record = cursor.fetchone()
        if record:
            employee = Employee(*record[:9])
            return employee
    
    # get employee bt email
    @staticmethod
    def get_employee_by_email(user_email):
        cursor = g.db.cursor()

        query = '''SELECT * from Employee WHERE email = %(email)s'''
        params = {"email" : user_email}
        cursor.execute(query, params)
        record = cursor.fetchone()
        if record:
            employee = Employee(*record[:9])
            # print("emp: ", employee.__dict__)
            return employee.__dict__

    def save(self):
        """Inserts employee record in the database"""

        cursor = g.db.cursor()

        query = '''INSERT INTO Employee(_id, first_name, last_name, email, password, phone, designation, is_admin, created_by)
                VALUES (%(_id)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s, %(phone)s, %(designation)s, %(is_admin)s, %(created_by)s)'''
        cursor.execute(query, self.__dict__)
        g.db.commit()

    def delete(self):
        """Deletes employee record from the database by matching on employee id"""

        cursor = g.db.cursor()

        query = '''UPDATE Employee SET is_active = false WHERE _id = %(_id)s'''
        params = {'_id': self._id}
        cursor.execute(query, params)
        g.db.commit()

    
    def update(self, params):
        """Updates employee record"""
    
        cursor = g.db.cursor()

        # forms update query based on fields to be updated
        query = '''UPDATE Employee SET '''

        for field in self.__dict__.keys():
            if field in params:
                self.__dict__[field] = params[field]
                query = query + f'{field}=%({field})s,'

        query = query[:-1] + f' WHERE _id=%(_id)s'

        cursor.execute(query, self.__dict__)
        g.db.commit()
    

    @staticmethod
    def is_admin(id):
        """Checks if the user is admin 

        Args:
            id (str): Employee id
        Returns:
            bool: if employee is admin or not
        """

        cursor = g.db.cursor()

        query = '''SELECT is_admin FROM Employee WHERE _id = %(_id)s'''
        params = {'_id': id}
        cursor.execute(query, params)

        record = cursor.fetchone()

        if record:
            return record[0]


    