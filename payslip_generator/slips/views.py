from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelform_factory
from django.http import HttpResponse
from .models import Company, Employee, Payslip
from .forms import CompanyForm, EmployeeForm, PayslipForm, EarningFormSet, DeductionFormSet

def create_payslip(request):
    # Create in-memory (unsaved) instances for formsets
    company = Company()
    employee = Employee(company=company)
    payslip = Payslip(company=company, employee=employee)

    if request.method == 'POST':
        cform = CompanyForm(request.POST, instance=company, prefix='company')
        eform = EmployeeForm(request.POST, instance=employee, prefix='employee')
        pform = PayslipForm(request.POST, instance=payslip, prefix='payslip')
        efs = EarningFormSet(request.POST, instance=payslip, prefix='earn')
        dfs = DeductionFormSet(request.POST, instance=payslip, prefix='ded')

        if cform.is_valid() and eform.is_valid() and pform.is_valid() and efs.is_valid() and dfs.is_valid():
            # Save objects
            company = cform.save()
            employee = eform.save(commit=False)
            employee.company = company
            employee.save()
            payslip = pform.save(commit=False)
            payslip.company = company
            payslip.employee = employee
            payslip.save()
            efs.instance = payslip
            dfs.instance = payslip
            efs.save()
            dfs.save()

            if 'preview' in request.POST:
                return redirect('slips:detail', pk=payslip.pk)
            elif 'download' in request.POST:
                return redirect('slips:pdf', pk=payslip.pk)
            return redirect('slips:detail', pk=payslip.pk)

    else:
        cform = CompanyForm(prefix='company')
        eform = EmployeeForm(prefix='employee')
        pform = PayslipForm(prefix='payslip')
        efs = EarningFormSet(prefix='earn', instance=payslip)
        dfs = DeductionFormSet(prefix='ded', instance=payslip)

    return render(request, 'slips/payslip_form.html', {
        'cform': cform, 'eform': eform, 'pform': pform,
        'earn_formset': efs, 'ded_formset': dfs
    })

def payslip_detail(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    return render(request, 'slips/payslip_detail.html', {'payslip': payslip})

def payslip_pdf(request, pk):
    """Render a PDF using xhtml2pdf if installed; otherwise return HTML with a note."""
    payslip = get_object_or_404(Payslip, pk=pk)
    try:
        from django.template.loader import get_template
        from xhtml2pdf import pisa
        template = get_template('slips/payslip_pdf.html')
        html = template.render({'payslip': payslip})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=payslip_{payslip.pk}.pdf'
        pisa.CreatePDF(html, dest=response)
        return response
    except Exception as e:
        # Fallback to HTML if xhtml2pdf not available
        return render(request, 'slips/payslip_pdf.html', {'payslip': payslip, 'pdf_error': str(e)})
