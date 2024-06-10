from django.urls import path
from .views import *
urlpatterns = [
    path('admin_register/', admin_register,name="admin_register"),
    path('admin_login/', admin_login,name="admin_login"),
    path('logout/',admin_logout,name="admin_logout"),
    path('employee_list/', employee_list_data,name="employee_list_data"),
    path("list_ajax/",employee_list,name="employee_list"),
    path("create_employee/",create_employee,name="create_employee"),
    path('delete_employee/', delete_employee, name='delete_employee'),
    path("get_employee_details/",get_employee_details,name="get_employee_details"),
    path("update_employee/<int:id>",update_employee,name="update_employee")
]