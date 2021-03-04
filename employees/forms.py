from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

class AddEmployeeForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)
	role = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label = "Pick a role")
	designation = forms.CharField()
	salary = forms.IntegerField()
	
	class Meta:
		model = User
		fields = [
			"first_name",
			"last_name",
			"username",
			"email",
			"password"
		]
	
	def clean_password(self):
		p1 = self.cleaned_data.get('password')
		p2 = self.cleaned_data.get('confirm_password')
		
		if p1 != p2:
			pass
			#raise forms.ValidationError("Passwords not matching")
		return p1
	
	def __init__(self, *args, **kwargs):
		if kwargs.get('instance'):
			initial = kwargs.setdefault('initial', {})
			if kwargs['instance'].groups.all():
				initial['role'] = kwargs['instance'].groups.all()[0]
			else:
				initial['role'] = None
		forms.ModelForm.__init__(self, *args, **kwargs)
		
	def save(self):
		password = self.cleaned_data.pop('password')
		role = self.cleaned_data.pop('role')
		designation = self.cleaned_data.pop('designation')
		salary = self.cleaned_data.pop('salary')
		
		u = super().save()
		
		u.groups.set([role])
		u.set_password(password)
		u.profile.designation = designation
		u.profile.salary = salary
		u.save()
		return u


class EditEmployeeForm(forms.ModelForm):
	designation = forms.CharField()
	salary = forms.IntegerField()
	role = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label = "Choose new role")
	
	class Meta:
		model = User
		fields = [
			"first_name",
			"last_name",
			"username",
			"email",
		]
		
	def __init__(self, *args, **kwargs):
		if kwargs.get('instance'):
			initial = kwargs.setdefault('initial', {})
			if kwargs['instance'].groups.all():
				initial['role'] = kwargs['instance'].groups.all()[0]
				initial['designation'] = kwargs['instance'].profile.designation
				initial['salary'] = kwargs['instance'].profile.salary
			else:
				initial['role'] = None
		forms.ModelForm.__init__(self, *args, **kwargs)
		
	def save(self):
		role = self.cleaned_data.pop('role')
		designation = self.cleaned_data.pop('designation')
		salary = self.cleaned_data.pop('salary')
		
		u = super().save()
		
		u.groups.set([role])
		u.profile.designation = designation
		u.profile.salary = salary
		u.save()
		return u