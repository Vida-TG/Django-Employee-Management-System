from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ems.decorators import role_required
from django.urls import reverse, reverse_lazy
from employees.forms import AddEmployeeForm, EditEmployeeForm
from django.contrib.auth.models import User
from django.views.generic import (
	CreateView,
	UpdateView,
	DeleteView,
)

decorators = [login_required, role_required(["HR", "Admin"])]
admin_decorators = [login_required, role_required(["Admin"])]


# Create your views here.

#login is always required to access anything about employees
@login_required
def employee_list(request):
	all_employees = User.objects.all()
	context = { 'employees' : all_employees }
	return render(request, 'employee/list.html', context)


@login_required
def employee_details(request, id=None):
	employee = get_object_or_404(User, id=id)
	context = { 'employee' : employee }
	return render(request, 'employee/details.html', context)


@method_decorator(admin_decorators, name="dispatch")
class EmployeeDelete(DeleteView):
	queryset = User.objects.all()
	template_name = 'employee/delete.html'
	context_object_name = "to_be_deleted"
	success_url = reverse_lazy('employee_list')


@method_decorator(decorators, name="dispatch")
class EmployeeAdd(CreateView):
	template_name = "employee/create.html"
	form_class = AddEmployeeForm
	
	def post(self, request, *args, **kwargs):
		form = AddEmployeeForm(request.POST)
		context = {"form":form}
		
		if form.is_valid():
			u = form.save()
			pk = u.id
			return redirect (reverse("employee_details", kwargs={'id':pk}))
		return render(request, self.template_name, context)

@method_decorator(login_required, name="dispatch")
class EmployeeEdit(UpdateView):
	template_name = "employee/edit.html"
	queryset = User.objects.all()
	form_class = EditEmployeeForm
	
	def post(self, request, pk=None, *args, **kwargs):
		print(pk)
		u = User.objects.get(id=pk)
		form = EditEmployeeForm(request.POST, instance=u)
		context = {"form":form}
		if form.is_valid():
			form.save()
			return redirect (reverse("employee_details", kwargs={'id':pk}))
		return render(request, self.template_name, context)

#python manage.py runserver
