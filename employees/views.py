from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Min, Max, Avg

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def _compute_deduction(self, country: str, gross: float) -> float:
        country = country.strip().lower()
        if country == 'india':
            return 0.10 * gross
        elif country in ('united states', 'usa', 'us', 'united states of america'):
            return 0.12 * gross
        else:
            return 0.0

    @action(detail=True, methods=['get'], url_path='calculate-salary')
    def calculate_salary(self, request, pk=None):
        employee = self.get_object()
        gross = request.query_params.get('gross')
        if gross is None:
            return Response({'error': 'gross parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            gross_val = float(gross)
        except (ValueError, TypeError):
            return Response({'error': 'gross must be a number'}, status=status.HTTP_400_BAD_REQUEST)
        if gross_val < 0:
            return Response({'error': 'gross must be non-negative'}, status=status.HTTP_400_BAD_REQUEST)

        deduction = self._compute_deduction(employee.country, gross_val)
        net = gross_val - deduction
        return Response({
            'employee_id': employee.id,
            'gross': gross_val,
            'deduction': deduction,
            'net': net,
        })


class SalaryMetricsByCountry(APIView):
    def get(self, request, country):
        qs = Employee.objects.filter(country__iexact=country)
        metrics = qs.aggregate(
            minimum=Min('salary'),
            maximum=Max('salary'),
            average=Avg('salary'),
        )
        return Response(metrics)


class SalaryMetricsByJob(APIView):
    def get(self, request, job_title):
        qs = Employee.objects.filter(job_title__iexact=job_title)
        metrics = qs.aggregate(average=Avg('salary'))
        return Response(metrics)
