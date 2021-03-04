from django.urls import path
from employees import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add-employee/', views.EmployeeAdd.as_view(), name='employee_add'),
    path('<int:id>/employee-details/', views.employee_details, name='employee_details'),
    path('<int:pk>/edit-employee/', views.EmployeeEdit.as_view(), name='employee_edit'),
    path('<int:pk>/delete-employee/', views.EmployeeDelete.as_view(), name='employee_delete'),
]