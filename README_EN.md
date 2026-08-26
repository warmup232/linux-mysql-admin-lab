# linux-mysql-admin-lab
Linux and MySQL Server Administration Lab
# Linux & MySQL Server Administration Lab

Personal hands-on project focused on Linux server
and MySQL database administration.

## Environment

- Ubuntu Server
- MySQL
- VMware Workstation
# Company Management API

A RESTful backend API for managing employees, departments, and projects.

## Tech Stack

- Python
- Flask
- MySQL
- REST API
- Linux / Ubuntu
- Git / GitHub

## Database

The application uses a relational MySQL database with:

- Departments
- Employees
- Projects
- Foreign key relationships
- Unique constraints
- Timestamp tracking

## Database Security

The application does not use the MySQL root account.

A dedicated application user is created with limited permissions:

- SELECT
- INSERT
- UPDATE
- DELETE

This follows the principle of least privilege.

## API Endpoints

### Employees

| Method | Endpoint | Description |
|---|---|---|
| GET | `/employees` | Get all employees |
| GET | `/employees/<id>` | Get employee by ID |
| POST | `/employees` | Create employee |
| PUT | `/employees/<id>` | Update employee |
| DELETE | `/employees/<id>` | Delete employee |

## Example Response

```json
{
  "id": 1,
  "name": "Kim Minsoo",
  "email": "minsoo@example.com",
  "department": "IT"
}
Database Setup

Run the SQL scripts in order:

database/01_schema.sql
database/02_seed.sql
database/03_permissions.sql
## Project Structure

company-management-api/
├── app/
│   └── app.py
├── database/
│   ├── 01_schema.sql
│   ├── 02_seed.sql
│   └── 03_permissions.sql
├── .gitignore
├── requirements.txt
└── README.md
Security Note

Database credentials are intentionally excluded from source control.
