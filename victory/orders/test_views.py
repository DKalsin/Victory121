from django.test import TestCase, Client
from .models import Order, Comment
from django.shortcuts import reverse


def setup_order():
    return Order.objects.create(
            title='test order',
            description='fix printer',
            status=Order.Status.NEW)


class TestCaseWithClient(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()


class IndexTest(TestCaseWithClient):
    def test_empty(self):
        response = self.client.get(reverse('orders:index'))
        self.assertEqual(len(response.context['order_list']), 0)

    def test_orders(self):
        order = setup_order()
        response = self.client.get(reverse('orders:index'))
        self.assertEqual(len(response.context['order_list']), 1)
        self.assertContains(response, order.title)
        self.assertTemplateUsed(response, 'orders/index.html')


class DetailedTest(TestCaseWithClient):
    def test_not_exists(self):
        response = self.client.get(reverse('orders:detail', args=[10]))
        self.assertEqual(response.status_code, 404)

    def test_order(self):
        order = setup_order()
        response = self.client.get(reverse('orders:detail', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/detail.html')
        self.assertContains(response, order.title)
        self.assertContains(response, order.description)


class AddCommentTest(TestCaseWithClient):
    def test_create(self):
        order = setup_order()
        comments_count = Comment.objects.count()
        response = self.client.post(
            reverse('orders:add_comment', args=[order.id]),
            data={'text': 'new comment'}
        )
        self.assertRedirects(
            response,
            reverse('orders:detail', args=[order.id])
        )
        self.assertEqual(Comment.objects.count(), comments_count + 1)


class NewOrderTest(TestCaseWithClient):
    def test_create(self):
        self.client.post(
            reverse('orders:new_order'),
            data={'title': 'new', 'description': 'new'}
        )
        self.assertEqual(Order.objects.get(pk=1).status, Order.Status.NEW)
