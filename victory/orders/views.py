from django.shortcuts import  get_object_or_404
from django.views import generic

from .models import Order, Comment


class CommentCreateView(generic.CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        form.instance.order = get_object_or_404(Order, pk=self.kwargs.get('pk', '-1'))
        return super().form_valid(form)


class OrderCreateView(generic.CreateView):
    model = Order
    fields = ['title', 'description', 'assignee', 'status']
    initial = {'status': 0}

    def form_valid(self, form):
        if form.instance.status is None:
            form.instance.status = Order.Status.NEW
        return super().form_valid(form)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_form_class().template_name = 'orders/order_form_template.html'


class OrderUpdateView(generic.UpdateView):
    model = Order
    fields = ['title', 'description','status', 'assignee', ]
    template_name = 'orders/detail.html'
    extra_context = {'comment_form': CommentCreateView().get_form_class()}


class OrderListView(generic.ListView):
    template_name = 'orders/index.html'

    def get_queryset(self):
        return Order.objects.order_by('-updated')
