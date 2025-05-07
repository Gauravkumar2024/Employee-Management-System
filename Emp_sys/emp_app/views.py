from django.shortcuts import render
from emp_app.models import Department,Role,Employee
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.contrib import messages  # Import message framework
# Create your views here.
def index(request):
    return render(request,'index.html')

def view_emp(request):
    results=Employee.objects.all()
    context={
        'emp':results
    }
    print(context)
    return render(request,'view_emp.html',context)

def add_emp(request):
    if request.method == 'POST':
         
        first_name = request.POST['first_name']
        last_name =request.POST['last_name']
        dept = int(request.POST['dept'])
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        role = int(request.POST['role'])
        phone = int(request.POST['phone'])
        # hire_date = request.POST['hire_date']

        department =Department.objects.get(id=dept)
        role_in = Role.objects.get(id=role)
        new_emp = Employee(first_name= first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, dept = department, role = role_in, hire_date = datetime.now())
        new_emp.save()
        return HttpResponse('Employee added Successfully')
        # print('dept',department)
        # return HttpResponse('<h1>here</h1>')
    else:
      departments = Department.objects.all()
      roles = Role.objects.all()
      return render(request,'add_emp.html',{'departments': departments, 'roles': roles})

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Employee  # Import your Employee model

def remove_emp(request):
    # Get the employee ID from the request
    record_id = request.GET.get('id')
    success_message = None

    if record_id:
        try:
            # Retrieve and delete the employee record
            rec = Employee.objects.get(id=record_id)
            rec.delete()
            # Set success message
            messages.success(request, f"Employee {rec.first_name} {rec.last_name} (ID: {rec.id}) deleted successfully.")
        except Employee.DoesNotExist:
            messages.error(request, "The selected employee does not exist.")

        # Redirect to the same page with a success message
        return redirect('remove_emp')
    # Get all employees
    result = Employee.objects.all()

    # Get success message from the query parameters
    # success_message = request.GET.get('success_message', None)

    # Pass employee list and success message to the template
    context = {
        'emp': result,
        'success_message': success_message,
    }

    return render(request, 'remove_emp.html', context)


def filter_emp(request):
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dept_id = request.POST.get('dept')
        emps=Employee.objects.all()
        print(first_name,last_name,dept_id)
        
        if first_name:
            emps=emps.filter(first_name__icontains=first_name)
            # The filter() method is used to retrieve records from the database that match the given conditions.
            # It returns a QuerySet, which is a collection of objects from the database that meet the specified criteria
        if last_name:
            emps=emps.filter(last_name__icontains=last_name)
        if dept_id:
            emps = emps.filter(dept__id=int(dept_id))
        context={
        'emp':emps
               }
        print(f"Filters: First Name={first_name}, Last Name={last_name}, Dept ID={dept_id}")

        return render(request,'view_emp.html',context)
    department =Department.objects.all()
    return render(request,'filter_emp.html',{'departments': department})