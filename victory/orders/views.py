# from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Order, Comment, User
from .forms import OrderForm, UserForm


class CommentCreateView(generic.CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        form.instance.order = get_object_or_404(Order, pk=self.kwargs.get('pk', '-1'))
        form.instance.author = self.request.user
        return super().form_valid(form)


class OrderCreateView(generic.CreateView):
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    extra_context = {
        'user_form': UserForm(),
    }

    def form_valid(self, form):
        user_form = UserForm(self.request.POST)
        try:
            user = User.objects.get(username=user_form.instance.username)
        except Exception:  # pylint: disable=broad-except
            if not user_form.is_valid():
                context = self.get_context_data()
                context['user_form'] = user_form
                return render(self.request,
                            self.template_name,
                            context)
            user = user_form.save()
        form.instance.client = user
        return super().form_valid(form)


class OrderUpdateView(generic.UpdateView):
    form_class = OrderForm
    model = Order
    template_name = 'orders/detail.html'
    extra_context = {
        'comment_form': CommentCreateView().get_form_class(),
    }


class OrderListView(generic.ListView):

    def get_queryset(self):
        return Order.objects.exclude(status=Order.Status.FIXED).order_by('-updated')
