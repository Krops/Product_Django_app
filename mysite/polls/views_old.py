
from django.http import Http404
from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from .models import Poll,Choice
from django.shortcuts import render_to_response

def index(request):
    latest_question_list = Poll.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
    '''latest_question_list = Poll.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = RequestContext(request, {
        'latest_question_list': latest_question_list,
    })
    return HttpResponse(template.render(context))'''
    #output = ', '.join([p.question for p in latest_question_list])
    #return HttpResponse(output)

def detail(request, poll_id):
    '''try:
        question = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404("Question does not exist")'''
    question = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/detail.html', {'poll': question})

def results(request, poll_id):
    question = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll': question})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))