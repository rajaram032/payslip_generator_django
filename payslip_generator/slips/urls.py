from django.urls import path
from . import views

app_name = 'slips'

urlpatterns = [
    path('', views.create_payslip, name='create'),
    path('payslip/<int:pk>/', views.payslip_detail, name='detail'),
    path('payslip/<int:pk>/pdf/', views.payslip_pdf, name='pdf'),
]
