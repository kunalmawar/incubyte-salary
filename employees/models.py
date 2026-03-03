from django.db import models


class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=12, decimal_places=2)

    def clean(self):
        # ensure salary is non-negative
        from django.core.exceptions import ValidationError

        if self.salary < 0:
            raise ValidationError({'salary': 'Salary must be non-negative'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.job_title})"
