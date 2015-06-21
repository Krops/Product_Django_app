from django.shortcuts import get_object_or_404, render
from .models import Product, Post, Vote
from django.views import generic
from django import forms

# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.shortcuts import redirect

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    #return HttpResponseRedirect(reverse('product:list'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def my_view(request):
    messages.add_message(request, 50, 'A serious error occurred.')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            if not request.user.is_authenticated():
                #return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
            # Return a 'disabled account' error message
            ...
    else:
        raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        # Return an 'invalid login' error message.
class IndexView(generic.ListView):
    template_name = 'product/list.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Product.objects.order_by('created_at')
'''def authorized(request):
    if request.user.is_authenticated():
        nope'''
def detail(request,product_id):
    product_list = Product.objects.order_by('created_at')[:5]
    product = get_object_or_404(Product, pk=product_id)
    context = {'product_list':product_list,'product':product}
    context.update(csrf(request))
    return render(request, 'product/detail.html', context)
def add_comment(request, product_id):
    #product = get_object_or_404(Product, pk=product_id)
    comment = Post(title="goog",body=request.POST['body'],product_id=product_id,author_id=request.user.id)
    #author = post["author"]
    comment.save()
    return HttpResponseRedirect(reverse('product:detail', args=(product_id,)))
def vote(request, product_id):
    p = get_object_or_404(Product, pk=product_id)
    try:
        if request.user.is_authenticated():
            print('hello')
            #print(Vote.objects.raw('SELECT id FROM product_vote WHERE product_id=1 and author_id=1 and rate=True')[0].id)
            try:
                if Vote.objects.raw('SELECT id FROM product_vote WHERE product_id=%s and author_id=%s and rate=True',product_id,request.user.id) > 0:
                    Vote.objects.raw('UPDATE product_vote SET rate=False WHERE product_id= %s and author_id= %s',product_id,request.user.id)
                #p.choice_set.get(pk=request.POST['choice'])
                    p.rate -= 1
                    p.save()
            except:
                #if Vote.objects.raw('SELECT id FROM product_vote WHERE product_id=1 and author_id=1 and rate=False')[0].id>0:
                print(product_id,request.user.id)
                voted = Vote(rate=True,product_id=product_id,author_id=request.user.id)
                voted.save()
                p.rate += 1
                p.save()
        else:
            return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
        
    except (KeyError, Product.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'product/detail.html', {
            'product': p,
            'error_message': "You didn't select a choice.",
        })


    return HttpResponseRedirect(reverse('product:detail', args=(p.id,)))
        