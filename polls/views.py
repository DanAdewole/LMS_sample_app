from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

# from django.http import Http404
# from django.template import loader

from .models import Question, Choices

# Create your views here.

# the old normal view

# def index(request):
# 	# written with HttpResponse here
# 	"""
# 	# latest_question_list = Question.objects.order_by('-pub_date')[:5]
# 	# template = loader.get_template('polls/index.html')
# 	# context = {
# 	# 	'latest_question_list': latest_question_list,
# 	# }

# 	# # views without templates -->
# 	# # output = ', '.join([q.question_text for q in latest_question_list])

# 	# return HttpResponse(template.render(context, request))
# 	"""

# 	# index view rewritten
# 	latest_question_list = Question.objects.order_by('-pub_date')[:5]
# 	context = {'latest_question_list': latest_question_list}
# 	return render(request, 'polls/index.html', context)

# def detail(request, question_id):
# 	# trying to raise errors 
# 	"""
# 	try:
# 		return HttpResponse("You're looking at question %s." % question_id)
# 	except Question.DoesNotExist:
# 		raise Http404("Question does not exist")
# 	return render(request, 'polls/detail.html', {'question': question})
# 	"""

# 	# optimized way to raise errors
# 	question = get_object_or_404(Question, pk=question_id)
# 	return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
# 	# response = "You're looking at the results of question %s."
# 	question = get_object_or_404(Question, pk=question_id)
# 	return render(request, 'polls/results.html', {'question': question})


# the new generic view


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the last five published questions"""
		return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'


def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choices_set.get(pk=request.POST['choice'])
	except (KeyError, Choices.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing with POST data. 
		# This prevents data from being posted twice if a user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
