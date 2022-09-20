from django.shortcuts import reverse
from django.views import generic

from .forms import OrderForm
from .models import Order


class OrderCreate(generic.CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'merchandise/order_form.html'

    def get_success_url(self):
        return reverse('merchandise:order_create')

    def form_valid(self, form):
        sizes = form.cleaned_data['sizes']
        form.instance.items = dict(sorted([(size, sizes.count(size)) for size in sizes]))
        # send email
        return super().form_valid(form)
