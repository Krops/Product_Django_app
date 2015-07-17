import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth import get_user_model

from .forms import CommentForm

from .models import Product, Post


def create_product(name, description, slug, price):
    '''создадим продукт'''
    return Product.objects.create(name=name, description=description, slug=slug, price=price)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('product:products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Products")
        self.assertQuerysetEqual(response.context['product_list'], [])
        print('kek')

    def test_logined(self):
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'smith'})
        print('yes')
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Your and password didn't match. Please try again.")

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page.
        """
        create_product(name="HTC Desire", description='good phone', slug='kek', price=1000)
        response = self.client.get(reverse('product:products'))
        self.assertQuerysetEqual(
            response.context['product_list'],
            ['<Product: HTC Desire>']
        )


class ProductMethodTests(TestCase):
    def test_was_published_recently_with_future_product(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_product = Product(created_at=time)
        self.assertEqual(future_product.was_published_recently(), False)


class CommentFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('zoidberg')
        self.entry = Product.objects.create(name='pop', description='goood', slug='heh', price=1000)

    def test_init(self):
        CommentForm(entry=self.entry)

    def test_init_without_entry(self):
        with self.assertRaises(KeyError):
            CommentForm()

    def test_valid_data(self):
        form = CommentForm({
            'title': "Turanga Leela",
            'body': "Hi there",
        }, entry=self.entry)
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(comment.title, "Turanga Leela")
        self.assertEqual(comment.body, "Hi there")
        #self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.entry, self.entry)
        print('all good')

    def test_blank_data(self):

        form = CommentForm({}, entry=self.entry)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'title': ['required'],'body': ['required'],})
