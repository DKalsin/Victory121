from django.test import TestCase, Client
from .models import Order, Comment, User
from django.shortcuts import reverse


def setup_order():
    return Order.objects.create(
            title='test order',
            description='fix printer',
            status=Order.Status.NEW)


class TestCaseWithClient(TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user = User.objects.create(username='admin')
        self.client.force_login(self.user)


class ListOrderTest(TestCaseWithClient):
    def test_empty(self):
        response = self.client.get(reverse('orders:list_order'))
        self.assertEqual(len(response.context['order_list']), 0)

    def test_orders(self):
        order = setup_order()
        response = self.client.get(reverse('orders:list_order'))
        self.assertEqual(len(response.context['order_list']), 1)
        self.assertContains(response, order.title)
        self.assertTemplateUsed(response, 'orders/order_list.html')


class UpdateOrderTest(TestCaseWithClient):
    def test_not_exists(self):
        response = self.client.get(reverse('orders:update_order', args=[10]))
        self.assertEqual(response.status_code, 404)

    def test_order(self):
        order = setup_order()
        response = self.client.get(reverse('orders:update_order', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/detail.html')
        self.assertContains(response, order.title)
        self.assertContains(response, order.description)


class CreateCommentTest(TestCaseWithClient):
    def test_create(self):
        order = setup_order()
        comments_count = Comment.objects.count()
        response = self.client.post(
            reverse('orders:create_comment', args=[order.id]),
            data={'text': 'new comment'}
        )
        self.assertRedirects(
            response,
            reverse('orders:update_order', args=[order.id])
        )
        self.assertEqual(Comment.objects.count(), comments_count + 1)


class CreateOrderTest(TestCaseWithClient):
    def test_create(self):
        self.client.post(
            reverse('orders:create_order'),
            data={
                'username': '+77771234567',
                'title': 'new',
                'description': 'new',
                'status': '0',
                'email': 'noreply@ya.ru',
                'last_name': 'noname',
                'first_name': 'noname',
            }
        )
        self.assertEqual(Order.objects.get(pk=1).status, Order.Status.NEW)
