from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
import base64
from PIL import Image
from io import BytesIO
def decode_base64_image(base64_data):
    # Remove the data URL prefix if present
    if base64_data.startswith('data:image'):
        base64_data = base64_data.split(',')[1]
    
    # Decode the base64 data
    binary_data = base64.b64decode(base64_data)
    return binary_data
def employee_list(request):
    try:
        return render(request,"employee/list.html",{"employee":Employee.objects.all()})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
@csrf_exempt 
def get_employee_list(request):
    if request.method == "POST":
        return JsonResponse({"employee":list(Employee.objects.al())})
@csrf_exempt
def create_employee(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            if data.get("employee_id") and Employee.objects.get(id=data.get("employee_id")):
                employee=Employee.objects.get(id=data.get("employee_id"))
                Address.objects.create(employee=employee,hno=data.get("hno"),street=data.get("street"),city=data.get("city"),state=data.get("state"))
                
                WorkExperience.objects.create(employee=employee,companyName=data.get("companyName"),fromDate=data.get("fromDate"),toDate=data.get("toDate"),address=data.get("address"))
                
                Qualification.objects.create(employee=employee,qualificationName=data.get("qualificationName"),percentage=data.get("percentage"))
                
                Project.objects.create(employee=employee,title=data.get("title"),description=data.get("description"))
                
                return JsonResponse({'message': 'Employee Details successfully', 'employee_id': employee.id})
            else:
                employee = Employee.objects.create(name=data.get("name"), email=data.get("email"), age=data.get("age"), gender=data.get("gender"), phoneNo=data.get("phoneNo"))
            
            return JsonResponse({'message': 'Employee created successfully', 'employee_id': employee.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': str(e)}, status=500)

# @csrf_exempt
def employee_details(request,id):
    if request.method == 'POST' :
        Photo.objects.create(employee_id=id,img=request.FILES.get('photo'))
        
        return render(request,"employee/employee_details.html",{"employee":Employee.objects.get(id=id),
                                                # "address":Address.objects.filter(employee_id=id).first(),
                                                # "workExperience":WorkExperience.objects.filter(employee_id=id),
                                                # "qualification":Qualification.objects.filter(employee_id=id),
                                                # "project":Project.objects.filter(employee_id=id)
                                                })
    return render(request,"employee/employee_details.html",{"employee":Employee.objects.get(id=id),
                                                # "address":Address.objects.filter(employee_id=id).first(),
                                                # "workExperience":WorkExperience.objects.filter(employee_id=id),
                                                # "qualification":Qualification.objects.filter(employee_id=id),
                                                # "project":Project.objects.filter(employee_id=id)
                                                })

def upload_image(request):
    if request.method == 'POST':
        description = request.POST.get('employee_id')
        image_file = request.FILES.get('img')

        # Create a new UploadedImage instance and save it
        uploaded_image = Photo(employee=Employee.objects.get(id=id), description=description, image=image_file)
        uploaded_image.save()

        return redirect('upload_success')
    return render(request, 'upload_image.html')