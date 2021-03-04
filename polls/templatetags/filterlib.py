from polls.models import Question
from django import template

def recent_polls(n=5):
	polls = Question.objects.all().order_by("-created_at")
	return polls[0:n]

register = template.Library()
register.tag("recent_polls", recent_polls)
