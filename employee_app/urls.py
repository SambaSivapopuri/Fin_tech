from django.urls import path,include
from .views import *
urlpatterns = [
    path('create/', create_employee, name='createEmployee'),
    path('update/<int:employee_id>/', edit_employee, name='updateEmployee'),
    path('delete/<int:employee_id>/', delete_employee, name='deleteEmployee'),
    path('employee_detail/', employee_detail, name='employeedetail'),
    path("list/",employee_list,name="list"),
    ]
