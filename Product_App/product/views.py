from django.shortcuts import get_object_or_404, render
from .models import Product, Post, Vote
from django.views import generic
from django import forms
from django.db import connection
import sys
from datetime import datetime

# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def login_view(request):
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
            # Return a '        #return ('detail',(),{'slug':str(self.slug)})
        #print(reverse('detail', args=[str(self.slug)]))disabled account' error message
    else:
        raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        # Return an 'invalid login' error message.

class IndexView(generic.ListView):
    template_name = 'product/list.html'
    context_object_name = 'product_list'


    def get_queryset(self):
        """Return the last five published questions."""
        return Product.objects.order_by('created_at')
def products(request):
    product_list = Product.objects.order_by('created_at')
    sort = request.GET.get('sort')
    #products = Product.objects.all()
    print('hello')
    if sort is not None:
        product_list = product_list.order_by(sort)

        if headers[sort] == "des":
            product_list.reverse()
            headers[sort] = "asc"
        else:
            headers[sort] = "des"
    return render(request, 'product/list.html', {'product_list':product_list})

def detail(request,slug):
    product_list = Product.objects.order_by('created_at')[:5]
    product = get_object_or_404(Product,slug=slug)
    try:
        ldc = str(product.post_set.last().created)[:10].split("-")
        ldc = [int(i) for i in ldc]
        comments = product.post_set.filter(created__year=ldc[0],created__month=ldc[1],created__day=ldc[2])
        more_comments = product.post_set.exclude(created__year=ldc[0],created__month=ldc[1],created__day=ldc[2])
        more_comments.order_by('created_at')
    #print(comments,comments2)
        context = {'product_list':product_list,'product':product,'comments':comments,'more_comments':more_comments}
        context.update(csrf(request))
        return render(request, 'product/detail.html', context)
    except:
        context = {'product_list':product_list,'product':product}
        context.update(csrf(request))
        return render(request, 'product/detail.html', context)

def add_comment(request, slug):
    product_id = Product.objects.get(slug=slug).pk
    if request.user.id:
        author_id=request.user.id
    else:
        author_id=1
    body=request.POST['body']
    if len(body)>4:
        comment = Post(title="goog",body=request.POST['body'],product_id=product_id,author_id=author_id)
        comment.save()
        messages.add_message(request, messages.SUCCESS, 'Comment added.',fail_silently=True)
    else:
        messages.add_message(request, messages.ERROR, 'Comment too small.',fail_silently=True)
    return HttpResponseRedirect(reverse('product:detail', args=(slug,)))
def show_more_comments(request,slug):
    product_list = Product.objects.order_by('created_at')[:5]
    product = get_object_or_404(Product,slug=slug)
    ldc = str(product.post_set.last().created)[:10].split("-")
    ldc = [int(i) for i in ldc]
    print(ldc)
    comments = product.post_set.filter(created__year=ldc[0],created__month=ldc[1],created__day=ldc[2])
    if comments.count() < product.post_set.all().count():
        comments = comments + product.post_set.all()[:5]
    print(comments)
    context = {'product_list':product_list,'product':product,'comments':comments}
    context.update(csrf(request))
    return render(request, 'product/detail.html', context)

def vote(request, slug):
    p = get_object_or_404(Product, slug=slug)
    product_id= Product.objects.get(slug=slug).pk
    try:
        if request.user.is_authenticated():
            if Vote.objects.filter(rate=True, author_id=request.user.id,product_id=product_id).count() >0:
                vote_update(False,product_id,request.user.id)
                p.rate -= 1
                p.save()

            elif Vote.objects.filter(rate=False, author_id=request.user.id,product_id=product_id).count() >0:
                vote_update(True,product_id,request.user.id)
                p.rate += 1
                p.save()
                messages.add_message(request, messages.SUCCESS, 'Voted',fail_silently=True)
            elif Vote.objects.filter(author_id=request.user.id,product_id=product_id).count()==0:
                voted = Vote(rate=True,product_id=product_id,author_id=request.user.id)
                voted.save()
                p.rate += 1
                p.save()
                messages.add_message(request, messages.SUCCESS, 'Voted',fail_silently=True)

        else:
            return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
        
    except (KeyError, Product.DoesNotExist):
        # Redisplay the product.post_set.all()question voting form.
        return render(request, 'product/detail.html', {
            'product': p,
            'error_message': "Pleasure login.",
        })




    return HttpResponseRedirect(reverse('product:detail', args=(p.slug,)))

def vote_update(rate,product_id,author_id):
    cursor = connection.cursor()
    cursor.execute('UPDATE product_vote SET rate=%s WHERE product_id= %s and author_id= %s',[rate,product_id,author_id])

headers = {'name':'asc',
         'price':'asc',
         'rate':'asc',}
def table_view(request):
    sort = request.GET.get('sort')
    print('lil')
    products = Product.objects.all()
    if sort is not None:
        products = products.order_by(sort)

        if headers[sort] == "des":
            products.reverse()
            headers[sort] = "asc"
        else:
            headers[sort] = "des"
            products.order_by(sort)

    return HttpResponseRedirect(reverse('product',{'product_list':products}))
