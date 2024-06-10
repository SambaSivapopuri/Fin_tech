from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout,authenticate
import re
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import *
def admin_register(request):
    try:
        if request.method == "POST":
            user= User.objects.filter(username=request.POST["username"]).first()
            if user:
                return render(request,"admin.html",{"user_name":"Alerdy Present"})
            else:
                User.objects.create_user(username=request.POST["username"],email=request.POST["email"],password=request.POST["password"])
                return redirect("admin_login")
    except:
        return render(request,"admin.html")
    return render(request,"admin.html")

def check_email_or_not(input_string):
    pattern = r'@'
    if re.search(pattern, input_string):
        return True
    else:
        return False
def admin_login(request):    
    
    try:
        if request.method == "POST":
            if check_email_or_not(request.POST["username"]):
                user=User.objects.filter(email=request.POST["username"]).first()
                admin=authenticate(request,username=user.username,password=request.POST["password"])
                print(admin)
                if admin is not None:
                    login(request, admin)
                    
                    return redirect('employee_list_data') 
                else:
                    messages.error(request, 'Invalid username or password.')
            else:
                admin=authenticate(request,username=request.POST["username"],password=request.POST["password"])
                print(admin)
                if admin is not None:
                    login(request, admin)
                    
                    return redirect('employee_list_data')  
                else:
                    messages.error(request, 'Invalid username or password.')
    except:
        return render(request,"login.html",{"msg":"Somthing Error"})
    return render(request,"login.html")

@login_required
def admin_logout(request):
    logout(request)
    return redirect("admin_register")

def employee_list_data(request):
    try:
        return render(request,"employee_list.html",{})
    except:
        return redirect("admin_login")
@csrf_exempt 
def employee_list(request):
    try:
        if request.method == "POST":
            return JsonResponse({"data": list(Employee.objects.all().values())})
        else:
            return JsonResponse({"error": "Method not allowed"}, status=405)
    except:
        return JsonResponse({"error": "Error"}, status=405)

@csrf_exempt
def create_employee(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            employee = Employee.objects.create(name=data.get("name"), email=data.get("email"), age=data.get("age"), gender=data.get("gender"), phoneNo=data.get("phoneNo"))
            Address.objects.create(employee=employee,hno=data.get("hno"),street=data.get("street"),city=data.get("city"),state=data.get("state"))
                
            WorkExperience.objects.create(employee=employee,companyName=data.get("companyName"),fromDate=data.get("fromDate"),toDate=data.get("toDate"),address=data.get("address"))
            
            Qualification.objects.create(employee=employee,qualificationName=data.get("qualificationName"),percentage=data.get("percentage"))
            
            Project.objects.create(employee=employee,title=data.get("title"),description=data.get("description"),image=data.get("img"))
            return JsonResponse({"data":"scuessfully added.."})
        except:
            return JsonResponse({"data":"not Added.."})
        
@csrf_exempt
def delete_employee(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        try:
            employee = Employee.objects.get(id=employee_id)
            employee.delete()
            return JsonResponse({'success': True})
        except Employee.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Employee not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
@csrf_exempt
def get_employee_details(request):
    try:
        if request.method == 'POST':
            employee_id = request.POST.get('id')
            try:
                employee = Employee.objects.get(id=employee_id)
                address = Address.objects.filter(employee=employee).first()  # Assuming one-to-one relationship
                work = WorkExperience.objects.filter(employee=employee).first()  # Assuming one-to-one relationship
                qualification = Qualification.objects.filter(employee=employee).first()  # First qualification
                project = Project.objects.filter(employee=employee).first()  # First project

                # Convert employee data to JSON format
                employee_data = {
                    'id': employee.id,
                    'name': employee.name,
                    'email': employee.email,
                    'age': employee.age,
                    'gender': employee.gender,
                    "phoneNo":employee.phoneNo,
                    "address_data" : {
                    "hno":address.hno,
                    'street': address.street,
                    'city': address.city,
                    'state': address.state,
                    },
            
                "work_data" : {
                    'companyName': work.companyName,
                    'fromDate': work.fromDate,
                    'toDate': work.toDate,
                    "address":work.address
                },
        "qualification_data" : {
                    'qualificationName': qualification.qualificationName,
                    'percentage': qualification.percentage,
                } ,
                "project_data" : {
                    'title': project.title,
                    'description': project.description,
                    'image': project.image,
                } 
                
                }
                

                return JsonResponse({
                    'success': True,
                    'employee': employee_data,
                    
                })
            
            except Employee.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Employee not found'})
    except:
        return JsonResponse({'success': False,  'error': 'Invalid request method'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def update_employee(request,id):
    try:
        if request.method == "POST":
            data= json.loads(request.body)
            employee=Employee.objects.filter(id=id).update(
                name=data.get("name"), email=data.get("email"), age=data.get("age"), gender=data.get("gender"), phoneNo=data.get("phoneNo"))
            Address.objects.filter(employee_id=id).update(employee=employee,hno=data.get("hno"),street=data.get("street"),city=data.get("city"),state=data.get("state"))
                
            WorkExperience.objects.filter(employee_id=id).update(employee=employee,companyName=data.get("companyName"),fromDate=data.get("fromDate"),toDate=data.get("toDate"),address=data.get("address"))
            
            Qualification.objects.filter(employee_id=id).update(employee=employee,qualificationName=data.get("qualificationName"),percentage=data.get("percentage"))
            
            Project.objects.filter(employee_id=id).update(employee=employee,title=data.get("title"),description=data.get("description"))
        return JsonResponse({"data":"Updated"})
    except:
        pass
    return JsonResponse({"data":"Updated"})