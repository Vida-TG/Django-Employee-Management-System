from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from polls.models import Question, Choice, Vote
from polls.forms import QuestionEditForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ems.decorators import role_required
from django.views.generic import (
	DeleteView,
	UpdateView,
)

# Create your views here.

decorators = [login_required, role_required(["HR", "Admin"])]

@login_required
def index(request):
	questions = Question.objects.filter(status="active").order_by("-created_at")
	recent = Question.objects.all().order_by("-created_at")
	if len(recent) > 10:
		recent = recent[0:10]
	context = {'questions' : questions, 'recent':recent}
	return render(request, 'polls/index.html', context)


@login_required
def details(request, id=None):
	try:
		question = Question.objects.get(id=id)
	except:
		raise Http404
	context={'question' : question}
	return render(request, 'polls/details.html', context)


@login_required
def vote(request, id=None):
	u = User.objects.get(id=request.user.id)
	q = Question.objects.get(id=id)
	initial_vote = None
	if Vote.objects.filter(user=u, question=q).exists():
		initial_vote = Vote.objects.get(user=u, question=q)
		
	if request.method == "POST":
		data = request.POST
		if initial_vote:
			initial_vote.delete()
		
		Vote.objects.create(user=u, choice_id=data['vote'], question=q)
		return redirect(reverse('details', kwargs={'id':id}))
	context = {'question':q, 'initial_vote':initial_vote}
	return render(request, "polls/vote.html", context)


@method_decorator(decorators, name="dispatch")
class DeletePoll(DeleteView):
	queryset = Question.objects.all()
	template_name = "polls/delete_poll.html"
	success_url = reverse_lazy("home")
