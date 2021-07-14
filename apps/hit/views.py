# Create your views here.
# Django Core
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views import View

# Local apps
from apps.authentication.models import User
from apps.authentication.utils import check_big_boss, check_managers
from apps.hit.forms import HitsForm
from apps.hit.models import Hit
from config.views import BaseListView, BaseDetailView, BaseCreateView, BaseUpdateView


class HitsUrlsMixin:
    """Mixin create send information additional a view"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opts = {
            "urls": {
                "create": reverse("hit:hits_create"),
                "bulk": reverse("hit:hits_bulk"),
                "list": reverse("hit:hits_list"),
            }
        }
        if "site" in context:
            context.get("site").update(opts)
        else:
            context.update({"site": opts})
        return context


class HitsListView(HitsUrlsMixin, LoginRequiredMixin, BaseListView):
    """Class define list hits"""

    model = Hit
    template_name = "hit/hit_list.html"
    list_fields = ("assignee", "description", "target", "state")
    bulk_fields = ("assignee",)

    def get_queryset(self):
        """Overwrite method queryset apply filter depende the rol"""
        queryset = super().get_queryset()
        user = self.request.user
        if check_big_boss(user):
            return queryset
        elif check_managers(user):
            hitmans = User.objects.filter(managers=user)
            hitmans = [user.pk for user in hitmans]
            hitmans += [user.pk]
            return queryset.filter(assignee__in=list(hitmans))
        else:
            state = Hit.StatusChoices
            return queryset.filter(
                assignee=user, state__in=[state.ASSIGNED, state.COMPLETED, state.FAILED]
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if "site" in context:
            if check_big_boss(user) or check_managers(user):
                opts = {
                    "perm_create": True,
                    "perm_bulk": True,
                }
                context.get("site").update(opts)
        return context


class HitsDetailView(HitsUrlsMixin, LoginRequiredMixin, BaseDetailView):
    """Class define detail hits"""

    model = Hit
    template_name = "hit/hit_detail.html"
    detail_fields = ("assignee", "description", "target")


class HitsCreateView(HitsUrlsMixin, LoginRequiredMixin, BaseCreateView):
    """Class define create hits"""

    model = Hit
    form_class = HitsForm
    template_name = "base/base_form.html"
    success_url = reverse_lazy("hit:hits_list")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Method overwrite redirect detail"""
        return reverse(
            "hit:hits_detail",
            kwargs={
                "pk": self.object.id,
            },
        )


class HitsUpdateView(HitsUrlsMixin, LoginRequiredMixin, BaseUpdateView):
    model = Hit
    form_class = HitsForm
    template_name = "base/base_form.html"
    success_url = reverse_lazy("hit:hits_list")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Method overwrite redirect detail"""
        return reverse(
            "hit:hits_detail",
            kwargs={
                "pk": self.object.id,
            },
        )


class HitBulkUpdateView(LoginRequiredMixin, View):
    """Class define bulk hits"""

    model = Hit
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        model = self.model
        ids = request.POST.getlist("ids")
        field = request.POST.get("field")
        value = request.POST.get("value")

        if not self.request.user.has_perm(
            f"{model._meta.app_label}.update_{model._meta.model_name}"
        ):
            return HttpResponseForbidden()

        if not hasattr(model, field):
            return JsonResponse(
                {"error": "The indicated field does not exist."}, status=400
            )

        objects = model.objects.filter(id__in=ids)
        objects.update(**{field: value})
        return JsonResponse({"success": f"{len(objects)} updated objects."}, status=200)
