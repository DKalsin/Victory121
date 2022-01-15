# from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Order, Comment
from .forms import OrderForm


class CommentCreateView(generic.CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        form.instance.order = get_object_or_404(Order, pk=self.kwargs.get('pk', '-1'))
        return super().form_valid(form)


class OrderCreateView(generic.CreateView):
    form_class = OrderForm


class OrderUpdateView(generic.UpdateView):
    form_class = OrderForm
    model = Order
    template_name = 'orders/detail.html'
    extra_context = {'comment_form': CommentCreateView().get_form_class()}


class OrderListView(generic.ListView):

    def get_queryset(self):
        return Order.objects.order_by('-updated')
