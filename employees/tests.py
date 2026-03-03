from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from .models import Employee


class EmployeeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee1 = Employee.objects.create(
            full_name="Alice Smith",
            job_title="Developer",
            country="India",
            salary=6000.00,
        )
        self.employee2 = Employee.objects.create(
            full_name="Bob Jones",
            job_title="Developer",
            country="United States",
            salary=8000.00,
        )
        self.employee3 = Employee.objects.create(
            full_name="Carlos Rey",
            job_title="Manager",
            country="Spain",
            salary=9000.00,
        )

    def test_list_employees(self):
        url = reverse('employee-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_employee(self):
        url = reverse('employee-detail', args=[self.employee1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], "Alice Smith")

    def test_create_employee(self):
        url = reverse('employee-list')
        data = {
            'full_name': 'Dana White',
            'job_title': 'Tester',
            'country': 'Canada',
            'salary': '5000.00',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 4)

    def test_update_employee(self):
        url = reverse('employee-detail', args=[self.employee1.id])
        data = {'job_title': 'Senior Developer'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee1.refresh_from_db()
        self.assertEqual(self.employee1.job_title, 'Senior Developer')

    def test_delete_employee(self):
        url = reverse('employee-detail', args=[self.employee1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(id=self.employee1.id).exists())

    def test_calculate_salary_india(self):
        url = reverse('employee-calculate-salary', args=[self.employee1.id])
        response = self.client.get(url + '?gross=1000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data['deduction'], 100.0)
        self.assertAlmostEqual(response.data['net'], 900.0)

    def test_calculate_salary_us(self):
        url = reverse('employee-calculate-salary', args=[self.employee2.id])
        response = self.client.get(url + '?gross=1000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data['deduction'], 120.0)
        self.assertAlmostEqual(response.data['net'], 880.0)

    def test_calculate_salary_other(self):
        url = reverse('employee-calculate-salary', args=[self.employee3.id])
        response = self.client.get(url + '?gross=1000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data['deduction'], 0.0)
        self.assertAlmostEqual(response.data['net'], 1000.0)

    def test_calculate_salary_missing_param(self):
        url = reverse('employee-calculate-salary', args=[self.employee1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('gross parameter required', response.data.get('error', ''))

    def test_calculate_salary_non_numeric(self):
        url = reverse('employee-calculate-salary', args=[self.employee1.id])
        response = self.client.get(url + '?gross=abc')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('gross must be a number', response.data.get('error', ''))

    def test_calculate_salary_negative(self):
        url = reverse('employee-calculate-salary', args=[self.employee1.id])
        response = self.client.get(url + '?gross=-100')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('gross must be non-negative', response.data.get('error', ''))

    def test_salary_metrics_country(self):
        url = reverse('salary-metrics-country', args=['India'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data['minimum'], 6000.00)
        self.assertAlmostEqual(response.data['maximum'], 6000.00)
        self.assertAlmostEqual(response.data['average'], 6000.00)

    def test_salary_metrics_job(self):
        url = reverse('salary-metrics-job', args=['Developer'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data['average'], 7000.00)
