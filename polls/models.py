from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

STATUS_CHOICE = (
	("active", "Active"),
	("inactive", "Closed"),
	)
class Question(models.Model):
	title = models.TextField()
	status = models.CharField(default="active", choices=STATUS_CHOICE, max_length=8)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	
	start_date = models.DateField(blank=True, null=True)
	end_date = models.DateField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def get_absolute_url(self):
		return reverse('details', kwargs={'id':self.id})
		
	def __str__(self):
		if len(self.title) > 50:
			return self.title[:50] + " . . ."
		else: return self.title
	
	@property
	def choices(self):
		return self.choice_set.all()



class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	text = models.TextField()
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		if len(self.text) > 50:
			return self.text[:50] + " . . ."
		else: return self.text
		
	@property
	def votes(self):
		return self.vote_set.count()



class Vote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		unique_together = ("user", "question")
		
	def __str__(self):
		return f"{self.user.last_name} - {self.choice.text}"
