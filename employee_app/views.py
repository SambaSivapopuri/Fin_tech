from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import *
import json

@csrf_exempt
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    address = Address.objects.filter(employee=employee).first()
    work_experience = WorkExperience.objects.filter(employee=employee)
    qualifications = Qualification.objects.filter(employee=employee)
    projects = Project.objects.filter(employee=employee)
    return JsonResponse({'employee': employee})

@csrf_exempt
def create_employee(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extract data
            name = data.get('name')
            email = data.get('email')
            age = data.get('age')
            gender = data.get('gender')
            phone_no = data.get('phoneNo')

            # Create Employee
            employee = Employee.objects.create(name=name, email=email, age=age, gender=gender, phoneNo=phone_no)

            # Create Address
            address_data = data.get('address')
            address = Address.objects.create(employee=employee, **address_data)

            # Create Work Experience
            work_experience_data = data.get('work_experience')
            for exp in work_experience_data:
                WorkExperience.objects.create(employee=employee, **exp)

            # Create Qualification
            qualification_data = data.get('qualifications')
            for qual in qualification_data:
                Qualification.objects.create(employee=employee, **qual)

            # Create Project
            project_data = data.get('projects')
            for proj in project_data:
                Project.objects.create(employee=employee, **proj)

            return JsonResponse({'message': 'Employee created successfully'}, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def edit_employee(request, employee_id):
    if request.method == 'POST':
        try:
            employee = Employee.objects.get(pk=employee_id)
            data = json.loads(request.body)

            # Update Employee
            employee.name = data.get('name')
            employee.email = data.get('email')
            employee.age = data.get('age')
            employee.gender = data.get('gender')
            employee.phoneNo = data.get('phoneNo')
            employee.save()

            # Update Address
            address = Address.objects.get(employee=employee)
            address_data = data.get('address')
            for key, value in address_data.items():
                setattr(address, key, value)
            address.save()

            # Update Work Experience
            work_experience_data = data.get('work_experience')
            for exp_data in work_experience_data:
                exp_id = exp_data.pop('id', None)
                if exp_id:
                    exp = WorkExperience.objects.get(pk=exp_id)
                    for key, value in exp_data.items():
                        setattr(exp, key, value)
                    exp.save()
                else:
                    exp_data['employee'] = employee
                    WorkExperience.objects.create(**exp_data)

            # Update Qualifications
            qualification_data = data.get('qualifications')
            for qual_data in qualification_data:
                qual_id = qual_data.pop('id', None)
                if qual_id:
                    qual = Qualification.objects.get(pk=qual_id)
                    for key, value in qual_data.items():
                        setattr(qual, key, value)
                    qual.save()
                else:
                    qual_data['employee'] = employee
                    Qualification.objects.create(**qual_data)

            # Update Projects
            project_data = data.get('projects')
            for proj_data in project_data:
                proj_id = proj_data.pop('id', None)
                if proj_id:
                    proj = Project.objects.get(pk=proj_id)
                    for key, value in proj_data.items():
                        setattr(proj, key, value)
                    proj.save()
                else:
                    proj_data['employee'] = employee
                    Project.objects.create(**proj_data)

            return JsonResponse({'message': 'Employee updated successfully'}, status=200)

        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
@csrf_exempt
def delete_employee(request, employee_id):
    if request.method == 'DELETE':
        try:
            employee = Employee.objects.get(pk=employee_id)
            
            # Delete related models
            Address.objects.filter(employee=employee).delete()
            WorkExperience.objects.filter(employee=employee).delete()
            Qualification.objects.filter(employee=employee).delete()
            Project.objects.filter(employee=employee).delete()

            # Delete employee
            employee.delete()

            return JsonResponse({'message': 'Employee deleted successfully'}, status=204)
        
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)

def employee_list(request):
    
    try:
        return render(request,"employee/list.html",{"employees":Employee.objects.all(),"gender":Gender.objects.all()})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
