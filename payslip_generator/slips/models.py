from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return f"{self.name} ({self.employee_id})" if self.employee_id else self.name

class Payslip(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, default='Payslip')
    pay_date = models.DateField()
    working_days = models.PositiveIntegerField(default=0)
    footer_amount_words = models.CharField(max_length=255, blank=True)

    @property
    def total_earnings(self):
        return sum(i.amount for i in self.earnings.all())

    @property
    def total_deductions(self):
        return sum(i.amount for i in self.deductions.all())

    @property
    def net_pay(self):
        return self.total_earnings - self.total_deductions

    def __str__(self):
        return f"{self.title} - {self.employee.name} ({self.pay_date})"

class EarningItem(models.Model):
    payslip = models.ForeignKey(Payslip, on_delete=models.CASCADE, related_name='earnings')
    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

class DeductionItem(models.Model):
    payslip = models.ForeignKey(Payslip, on_delete=models.CASCADE, related_name='deductions')
    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
