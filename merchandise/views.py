import secrets

from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import generic

from .forms import OrderForm
from .models import Order, Token


class OrderCreateView(generic.CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'merchandise/order_form.html'
    success_url = reverse_lazy('merchandise:order-done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(is_verified=True).values_list('items', flat=True)
        total = sum([sum(order.values()) for order in orders])
        goal = 30
        context['stats'] = {
            'value': total if total <= goal else goal,
            'max': goal,
            'percentage': round(total / goal * 100),
        }
        return context

    def form_valid(self, form):
        # save object with json type
        sizes = form.cleaned_data['sizes']
        form.instance.items = dict(sorted([(size, sizes.count(size)) for size in sizes]))
        order = form.save()

        # generate magic link
        token = Token.objects.create(
            key=secrets.token_urlsafe(16),
            order=order,
            expired_at=timezone.now() + timedelta(seconds=60 * 60),
        )

        # send email
        template = get_template('merchandise/order_verification_mail.txt')
        magic_link = self.request.build_absolute_uri(reverse('merchandise:order-verify') + f'?token={token.key}')
        send_mail(
            subject=_("Verify your order"),
            message=template.render({
                'name': order.first_name,
                'items': order.items.items(),
                'magic_link': magic_link,
                'expired_at': token.expired_at,
            }),
            from_email=None,
            recipient_list=[order.email],
        )
        return redirect(self.success_url)


class OrderSuccessView(generic.TemplateView):
    template_name = 'merchandise/order_success.html'


def verify_order(request):
    template_name = 'merchandise/verification_feedback.html'
    key = request.GET.get('token')

    if not key:  # Missing query
        return render(request, template_name, {
            'is_valid': False,
            'message': _("The link was malformed. Please make sure that you do not alter the link."),
        })

    try:  # Token not found
        token = Token.objects.get(key=key)
    except Token.DoesNotExist:
        return render(request, template_name, {
            'is_valid': False,
            'message': _("The token was malformed. Please make sure that you do not alter the token."),
        })

    if timezone.now() > token.expired_at:  # Token expired
        token.delete()
        return render(request, template_name, {
            'is_valid': False,
            'message': _("The token is expired. Please request a new one by contacting us."),
        })

    order = token.order
    order.is_verified = True
    order.save()

    token.delete()

    return render(request, template_name, {
        'is_valid': True,
        'message': _("Your order is completed. We will contact you when we ship your items."),
    })


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        orders = Order.objects.values_list('items', 'is_verified')
        total = {}
        for items, is_verified in orders:
            for item, amount in items.items():
                if item not in total.keys():
                    total[item] = [0, 0]

                total[item][0] += amount
                if is_verified:
                    total[item][1] += amount

        context['items_total'] = dict(sorted(total.items()))
        return context


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Order
    success_url = reverse_lazy('merchandise:order-list')
