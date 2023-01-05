from flask import g
from ...utils import make_response
from .constant import *
import re


class Employee:
    __tablename__: 'Employee'

    def __init__(self, id, first_name, last_name, email, password, phone, designation, is_active=True, is_admin=False):
        self._id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone
        self.designation = designation
        self.is_active = is_active
        self.is_admin = is_admin

    @staticmethod
    def get_employees():
        cursor = g.db.cursor()
        query = '''SELECT * FROM Employee WHERE is_active=true'''
        cursor.execute(query)
        records = cursor.fetchall()
        employees = []
        for employee_record in records:
            employee = Employee(*employee_record[:9])
            employees.append(employee.__dict__)

        return employees

    @staticmethod
    def get_employee_by_id(employee_id):
        cursor = g.db.cursor()

        query = '''SELECT * FROM Employee WHERE _id = %(_id)s AND is_active=true'''
        params = {'_id': employee_id}
        cursor.execute(query, params)
        record = cursor.fetchone()
        if record:
            employee = Employee(*record[:9])
            return employee

    def save(self):
        cursor = g.db.cursor()

        query = '''INSERT INTO Employee(_id, first_name, last_name, email, password, phone, designation, is_admin)
                VALUES (%(_id)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s, %(phone)s, %(designation)s, %(is_admin)s)'''

        cursor.execute(query, self.__dict__)
        g.db.commit()

    @staticmethod
    def delete_employee_by_id(employee_id):
        cursor = g.db.cursor()

        query = '''UPDATE Employee SET is_active = false WHERE _id = %(_id)s'''
        params = {'_id': employee_id}
        cursor.execute(query, params)
        g.db.commit()

    def delete(self):
        cursor = g.db.cursor()

        query = '''UPDATE Employee SET is_active = false WHERE _id = %(_id)s'''
        params = {'_id': self._id}
        cursor.execute(query, params)
        g.db.commit()
