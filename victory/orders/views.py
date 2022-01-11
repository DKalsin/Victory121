from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic.edit import CreateView

from .models import Order, Comment
from .forms import AddCommentForm


class IndexView(generic.ListView):
    template_name = 'orders/index.html'

    def get_queryset(self):
        return Order.objects.order_by('-updated')


class DetailView(generic.DetailView):
    model = Order
    template_name = 'orders/detail.html'
    extra_context = {'comment_form': AddCommentForm()}


def add_comment(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = AddCommentForm(request.POST, instance=Comment(order=order))
    if form.is_valid():
        form.save()
        return redirect('orders:detail', pk=order.id)
    return render(request, 'orders/detail.html', {'form': form})


class NewOrderView(CreateView):
    model = Order
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.status = Order.Status.NEW
        return super().form_valid(form)
