from django.contrib import admin
from .models import Company, Employee, Payslip, EarningItem, DeductionItem

class EarningInline(admin.TabularInline):
    model = EarningItem
    extra = 1

class DeductionInline(admin.TabularInline):
    model = DeductionItem
    extra = 1

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    inlines = [EarningInline, DeductionInline]
    list_display = ('title','employee','pay_date','net_pay')

admin.site.register(Company)
admin.site.register(Employee)
