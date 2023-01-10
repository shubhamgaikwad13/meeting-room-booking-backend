FETCH_EMPLOYEES_FAILED = "Failed to fetch employee records."
NO_EMPLOYEES_FOUND = "No employees in the database."
EMPLOYEE_NOT_FOUND = "Employee not found."
EMPLOYEE_ADDED = "Employee added successfully."
EMPLOYEE_DELETED = "Employee deleted successfully."
EMPLOYEE_ID_REQUIRED = "Employee id is required."
EMPLOYEE_FIRST_NAME_REQUIRED = "Employee first name is required."
EMPLOYEE_LAST_NAME_REQUIRED = "Employee last name is required."
EMPLOYEE_EMAIL_REQUIRED = "Employee email is required."
EMPLOYEE_PHONE_REQUIRED = "Employee phone is required."
EMPLOYEE_DESIGNATION_REQUIRED = "Employee designation is required."
EMPLOYEE_PASSWORD_REQUIRED = "Employee password is required."
EMPLOYEE_IS_ADMIN_REQUIRED = "Employee is_admin field is required."
EMPLOYEE_PHONE_LENGTH = "Employee contact number must be 10 digits."
EMPLOYEE_PHONE_INVALID = "Employee contact number is not valid."
ONLY_ADMIN_ADDS_USER = "Only admin can add the user."


def dup_message(value): return f"Duplicate entry for employee {value}."


DUP_ENTRY = ['PRIMARY', 'email', 'phone']
