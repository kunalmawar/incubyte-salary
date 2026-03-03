from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet, SalaryMetricsByCountry, SalaryMetricsByJob

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
    # metrics
    path('salary-metrics/country/<str:country>/', SalaryMetricsByCountry.as_view(), name='salary-metrics-country'),
    path('salary-metrics/job/<str:job_title>/', SalaryMetricsByJob.as_view(), name='salary-metrics-job'),
]
