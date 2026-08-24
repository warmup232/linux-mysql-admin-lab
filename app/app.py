import os

from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "app_user"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "company_db")
    )


# Health check
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Company Management API",
        "status": "running"
    })


# ============================================================
# Employees
# ============================================================

@app.route("/employees", methods=["GET"])
def get_employees():
    connection = None
    cursor = None

    try:
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

        return jsonify(cursor.fetchall())

    except Error:
        return jsonify({"error": "Database error"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    connection = None
    cursor = None

    try:
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

        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        return jsonify(employee)

    except Error:
        return jsonify({"error": "Database error"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route("/employees", methods=["POST"])
def create_employee():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("email"):
        return jsonify({
            "error": "name and email are required"
        }), 400

    connection = None
    cursor = None

    try:
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

        return jsonify({
            "message": "Employee created",
            "id": cursor.lastrowid
        }), 201

    except Error:
        if connection:
            connection.rollback()

        return jsonify({"error": "Database error"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    connection = None
    cursor = None

    try:
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
            return jsonify({"error": "Employee not found"}), 404

        return jsonify({
            "message": "Employee updated"
        })

    except Error:
        if connection:
            connection.rollback()

        return jsonify({"error": "Database error"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM employees
            WHERE id = %s
        """, (employee_id,))

        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Employee not found"}), 404

        return jsonify({
            "message": "Employee deleted"
        })

    except Error:
        if connection:
            connection.rollback()

        return jsonify({"error": "Database error"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ============================================================
# Departments
# ============================================================

@app.route("/departments", methods=["GET"])
def get_departments():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, name
            FROM departments
            ORDER BY id
        """)

        return jsonify(cursor.fetchall())

    except Error:
        return jsonify({"error": "Database error"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ============================================================
# Projects
# ============================================================

@app.route("/projects", methods=["GET"])
def get_projects():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.id,
                p.name,
                p.status,
                e.name AS employee
            FROM projects p
            LEFT JOIN employees e
                ON p.employee_id = e.id
            ORDER BY p.id
        """)

        return jsonify(cursor.fetchall())

    except Error:
        return jsonify({"error": "Database error"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route("/projects", methods=["POST"])
def create_project():
    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({
            "error": "name is required"
        }), 400

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO projects
                (name, employee_id, status)
            VALUES
                (%s, %s, %s)
        """, (
            data["name"],
            data.get("employee_id"),
            data.get("status", "ACTIVE")
        ))

        connection.commit()

        return jsonify({
            "message": "Project created",
            "id": cursor.lastrowid
        }), 201

    except Error:
        if connection:
            connection.rollback()

        return jsonify({"error": "Database error"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
