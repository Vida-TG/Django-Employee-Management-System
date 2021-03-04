from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	designation = models.CharField(max_length=10)
	salary = models.IntegerField(null=True, blank=True)
	
	class meta:
		ordering = ("-salary")
		
	def __str__(self):
		return f"{self.user.first_name} {self.user.last_name}"

@receiver(post_save, sender=User)
def user_created_or_updated(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	else:
		instance.profile.save()
