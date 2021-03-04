from django.core.exceptions import PermissionDenied

def role_required(allowed=[]):
	def decorator(func):
		def wrapper(request, *args, **kwargs):
			if request.user.role in allowed:
				return func(request, *args, **kwargs)
			else: raise PermissionDenied
		return wrapper
	return decorator
