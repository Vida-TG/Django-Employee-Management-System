
class RoleMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response
	def __call__(self, request):
		response = self.get_response(request)
		return response
	def process_view(self, request, view_func, *args, **kwargs):
		
		if request.user.is_authenticated:
			request.user.role = None
			groups = request.user.groups.all()
			if groups:
				request.user.role = groups[0].name
