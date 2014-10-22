from django.views import generic
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


class GetPublishedObjectMixin(object):
    """
    Get Object Mixin

    Retrieves the object if the request user is the owner, or if
    the object is published. Otherwise returns status 403
    """
    def get_object(self, **kwargs):
        gotten_object = super(GetPublishedObjectMixin, self) \
            .get_object(**kwargs)
        if gotten_object.owner != self.request.user:
            if gotten_object.published == 0:
                raise PermissionDenied()
        return gotten_object


class ListSortMixin(object):

    def get_sorted_queryset(self, default_sort='-modified_at'):
        sort_options = ['created_at', 'modified_at', 'name', 'owner']
        sort_by = self.request.GET.get('by', False)
        sort_order = int(self.request.GET.get('order', False))

        if not sort_order or sort_by not in sort_options:
            return self.model.objects.order_by(default_sort)

        sort_order = "{0}" if sort_order > 0 else "-{0}"
        sort = sort_order.format(sort_by)
        return self.model.objects.order_by(sort)


class HelpView(generic.TemplateView):
    template_name = "site/help.html"


class RegisterView(generic.FormView):
    template_name = "registration/register.html"
    model = settings.AUTH_USER_MODEL
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('login')

    def form_valid(self, form):
        messages.success(self.request, 'Thanks for registering. Please login with your new username and password.')
        return super(RegisterView, self).form_valid(form)