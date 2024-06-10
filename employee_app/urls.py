from django.urls import path,include
from .views import *
urlpatterns = [
    path("list/",employee_list,name="employee_list"),
    path("create_employee/",create_employee,name="create_employee"),
    path("employee/<int:id>",employee_details,name="employee_details")
    ]
