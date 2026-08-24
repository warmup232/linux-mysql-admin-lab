from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="app_user",
        password="YOUR_DATABASE_PASSWORD",
        database="company_db"
    )


# Health check
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Company Management API",
        "status": "running"
    })


# Get all employees
@app.route("/employees", methods=["GET"])
def get_employees():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.email,
            d.name AS department,
            e.created_at
        FROM employees e
        LEFT JOIN departments d
            ON e.department_id = d.id
        ORDER BY e.id
    """)

    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(employees)


# Get employee by ID
@app.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.email,
            d.name AS department,
            e.created_at
        FROM employees e
        LEFT JOIN departments d
            ON e.department_id = d.id
        WHERE e.id = %s
    """, (employee_id,))

    employee = cursor.fetchone()

    cursor.close()
    connection.close()

    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify(employee)


# Create employee
@app.route("/employees", methods=["POST"])
def create_employee():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("email"):
        return jsonify({
            "error": "name and email are required"
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO employees
            (name, email, department_id)
        VALUES
            (%s, %s, %s)
    """, (
        data["name"],
        data["email"],
        data.get("department_id")
    ))

    connection.commit()

    employee_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Employee created",
        "id": employee_id
    }), 201


# Update employee
@app.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE employees
        SET name = %s,
            email = %s,
            department_id = %s
        WHERE id = %s
    """, (
        data.get("name"),
        data.get("email"),
        data.get("department_id"),
        employee_id
    ))

    connection.commit()

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        return jsonify({"error": "Employee not found"}), 404

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Employee updated"
    })


# Delete employee
@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM employees
        WHERE id = %s
    """, (employee_id,))

    connection.commit()

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        return jsonify({"error": "Employee not found"}), 404

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Employee deleted"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
