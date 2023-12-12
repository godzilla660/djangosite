from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic


from polls.models import Choice, Question


# Create your views here.


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-publication_date")[:5]

    # latest_question_list = Question.objects.order_by("-publication_date")[:5]
    # context = {"latest_question_list": latest_question_list}
    # return render(request, "polls/index.html", context)

    # output = '*** '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


# def ResultsView(generic.DetailView):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question":question})
#     return HttpResponse("You're looking at the results of the question %s." % question_id)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
