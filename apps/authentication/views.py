from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from apps.authentication.forms import RegisterUserForm, HitmanUpdateForm
from apps.authentication.models import User
from config.views import BaseListView, BaseDetailView, BaseUpdateView
from .utils import check_big_boss, check_managers


class SignUpView(SuccessMessageMixin, CreateView):
    """Class define register de user"""

    form_class = RegisterUserForm
    template_name = "authentication/register.html"
    success_url = reverse_lazy("auth:login")
    success_message = "Your profile was created successfully"


class HitmanUrlsMixin:
    """Mixin create urls base"""

    def get_context_data(self, **kwargs):
        """Overwrite contexto"""
        context = super().get_context_data(**kwargs)
        urls = {"list": reverse("auth:hitman_list")}
        opts = {"title": "Hitman", "urls": urls}
        if "site" in context:
            context.get("site").update(opts)
        else:
            context.update({"site": opts})
        return context


class HitmanListView(HitmanUrlsMixin, LoginRequiredMixin, BaseListView):
    """Class define list de hitman"""

    model = User
    template_name = "hitman/hitman_list.html"
    list_fields = ("email", "get_full_name:full name", "state", "rol:roles")

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return self.handle_no_permission()
        if check_big_boss(user) or check_managers(user):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def get_queryset(self):
        """Overwrite method queryset apply filter depende the rol"""
        queryset = super().get_queryset().exclude(id=1)
        user = self.request.user
        if check_big_boss(user):
            return queryset
        if check_managers(user):
            hitmans = self.model.objects.filter(managers=user)
            hitmans = [user.pk for user in hitmans]
            hitmans += [user.pk]
            return queryset.filter(pk__in=list(hitmans))
        return queryset.none()


class HitmanDetailView(HitmanUrlsMixin, LoginRequiredMixin, BaseDetailView):
    """Class define the detail hitman"""

    model = User
    template_name = "hitman/hitman_detail.html"
    detail_fields = ("email", "first_name", "last_name")

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return self.handle_no_permission()
        if check_big_boss(user) or check_managers(user):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        """Overwrite get context data send list hitmans for users"""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        hitmans = User.objects.filter(managers=user)
        context.update({"hitmans": hitmans})
        return context


class AddFromManagersGroupView(HitmanUrlsMixin, LoginRequiredMixin, BaseUpdateView):
    """Class define add hitman to managers"""

    model = User
    form_class = HitmanUpdateForm
    template_name = "base/base_form.html"

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return self.handle_no_permission()
        if check_big_boss(user):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def get_success_url(self):
        """Method redirect detail hitman"""
        return reverse(
            "auth:hitman_detail",
            kwargs={
                "pk": self.object.id,
            },
        )

    def get_context_data(self, **kwargs):
        """Overwrite get context data send list hitmans for users"""
        context = super().get_context_data(**kwargs)
        if "site" in context:
            context.get("site").update({"title": "Add From Managers Group"})
        return context


# class RemoveFromManagersGroupView
