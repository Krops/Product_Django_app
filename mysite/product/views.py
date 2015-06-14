from django.shortcuts import get_object_or_404, render
from .models import Product, Post
from django.views import generic
from django import forms

# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse


def my_view(request):
    messages.add_message(request, 50, 'A serious error occurred.')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            messages.add_message(request, messages.INFO, 'Hello world.')
            # Redirect to a success page.
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
        return Product.objects.order_by('-created_at')
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
    comment = Post(title="goog",body=request.POST['body'],product_id=product_id)
    #author = post["author"]
    comment.save()
    return HttpResponseRedirect(reverse('product:detail', args=(product_id,)))

        