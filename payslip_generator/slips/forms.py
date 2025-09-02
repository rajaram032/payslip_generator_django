from django import forms
from django.forms import inlineformset_factory
from .models import Company, Employee, Payslip, EarningItem, DeductionItem

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'employee_id']

class PayslipForm(forms.ModelForm):
    class Meta:
        model = Payslip
        fields = ['title', 'pay_date', 'working_days', 'footer_amount_words']
        widgets = {
            'pay_date': forms.DateInput(attrs={'type': 'date'})
        }

EarningFormSet = inlineformset_factory(
    Payslip, EarningItem, fields=('title','amount'), extra=3, can_delete=True
)
DeductionFormSet = inlineformset_factory(
    Payslip, DeductionItem, fields=('title','amount'), extra=2, can_delete=True
)
