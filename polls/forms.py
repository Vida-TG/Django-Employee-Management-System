from django import forms
from .models import Question

class QuestionEditForm(forms.ModelForm):
	class Meta:
		model = Question
		
		exclude = [
			'created_by',
		]

