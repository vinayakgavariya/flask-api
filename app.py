import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Initial set of employees
employees = [
    {'id': 1, 'name': 'Ashley'},
    {'id': 2, 'name': 'Kate'},
    {'id': 3, 'name': 'Joe'},
    {'id': 4, 'name': 'Alex'}
]

# Variable to track the ID for the next employee
nextEmployeeId = 5

# Route to retrieve all employees
@app.route('/employees/', methods=['GET'])
def get_all_employees():
    return jsonify(employees)

# Alternate route to retrieve all employees (without trailing slash)
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

# Route to retrieve a specific employee by ID
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee_by_id(id: int):
    employee = get_employee(id)
    if employee is None:
        return jsonify({'error': 'Employee does not exist'}), 404
    return jsonify(employee)

# Function to get an employee by their ID
def get_employee(id):
    return next((e for e in employees if e['id'] == id), None)

# Function to validate employee properties
def employee_is_valid(employee):
    for key in employee.keys():
        if key != 'name':
            return False
    return True

# Route to create a new employee
@app.route('/employees', methods=['POST'])
def create_employee():
    global nextEmployeeId
    employee = json.loads(request.data)
    if not employee_is_valid(employee):
        return jsonify({'error': 'Invalid employee properties.'}), 400

    # Assign ID to the new employee and increment nextEmployeeId
    employee['id'] = nextEmployeeId
    nextEmployeeId += 1

    # Add the new employee to the list of employees
    employees.append(employee)

    # Return a 201 response with the location of the newly created employee
    return '', 201, {'location': f'/employees/{employee["id"]}'}

# Route to update an existing employee
@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id: int):
    employee = get_employee(id)
    if employee is None:
        return jsonify({'error': 'Employee does not exist.'}), 404

    updated_employee = json.loads(request.data)
    if not employee_is_valid(updated_employee):
        return jsonify({'error': 'Invalid employee properties.'}), 400

    # Update the existing employee with the new data
    employee.update(updated_employee)

    # Return the updated employee
    return jsonify(employee)

# Route to delete an existing employee
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id: int):
    global employees
    employee = get_employee(id)
    if employee is None:
        return jsonify({'error': 'Employee does not exist.'}), 404

    # Remove the employee from the list of employees
    employees = [e for e in employees if e['id'] != id]

    # Return the deleted employee
    return jsonify(employee), 200

# Run the Flask application
if __name__ == '__main__':
    app.run(port=5000)
