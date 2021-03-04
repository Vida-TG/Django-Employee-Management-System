from polls.models import Question

def poll_count(request):
	active_q = Question.objects.filter(status="active").count()
	
	return {'active_q':active_q}

