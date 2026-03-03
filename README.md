# Salary Kata

This Django project provides a simple API for managing employees and performing salary calculations/metrics.

## Setup

1. Create a Python virtual environment and activate it:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install django djangorestframework
   ```

3. Run migrations to create the SQLite database:

   ```bash
   python manage.py migrate
   ```

4. (Optional) create a superuser for admin access:

   ```bash
   python manage.py createsuperuser
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

## API Endpoints

All endpoints are prefixed with `/api/`.

### Employee CRUD

- `GET /api/employees/` - list all employees
- `POST /api/employees/` - create a new employee
- `POST /api/employees/bulk-create/` - create multiple employees in one request (expects JSON list)
- `GET /api/employees/{id}/` - retrieve employee by ID
- `PUT /api/employees/{id}/` - update employee
- `PATCH /api/employees/{id}/` - partial update
- `DELETE /api/employees/{id}/` - delete employee

Employee fields:
- `full_name` (string)
- `job_title` (string)
- `country` (string)
- `salary` (decimal, non-negative)

> **Note:** salary is validated to be non-negative; attempts to save a negative value will raise a validation error.

### Salary Calculation

Calculate net salary for an employee given a gross amount.

```
GET /api/employees/{id}/calculate-salary/?gross=<amount>
```

Deduction rules by country:

- India: 10% of gross
- United States: 12% of gross
- Others: no deductions

Response example:

```json
{
  "employee_id": 1,
  "gross": 5000.0,
  "deduction": 500.0,
  "net": 4500.0
}
```

### Salary Metrics

- `GET /api/salary-metrics/country/{country}/` - returns minimum, maximum, and average salary for the given country.

- `GET /api/salary-metrics/job/{job_title}/` - returns average salary for the given job title.

Response examples:

```json
{ "minimum": 3000.00, "maximum": 7000.00, "average": 5000.00 }
```

```json
{ "average": 6200.00 }
```

## Notes

- A SQLite database is used by default (`db.sqlite3` in the project root).
- The `rest_framework` package is required.
- Feel free to extend the logic or add authentication as needed.

## Testing

Automated tests are provided for the `employees` app covering CRUD operations, salary calculations and metrics.

Run them with:

```bash
python manage.py test employees
```

Make sure migrations have been applied before running tests (the test runner will create its own in-memory database by default).
