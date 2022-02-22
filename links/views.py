from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic

from .forms import ChangeOrderForm
from .models import Link


class IndexView(generic.ListView):
    template_name = 'links/index.html'
    model = Link
    queryset = Link.objects.filter(is_active=True)


@permission_required('links.change_link')
def change_order(request):
    links = Link.objects.all()
    if request.method == 'POST':
        form = ChangeOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('links:change_order_done')
    else:
        form = ChangeOrderForm()
    return render(request, 'links/change_order.html', {'form': form, 'links': links})


class ChangeOrderDoneView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'links/change_order_done.html'
