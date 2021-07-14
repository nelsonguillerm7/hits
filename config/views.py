from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)

from config.utils import Field


class BaseSiteMixin:
    def get_context_data(self, **kwargs):
        """Overwrite get context data add items common"""
        context = super().get_context_data(**kwargs)
        if hasattr(self, "model") and self.model is not None:
            opts = {
                "title": self.model._meta.verbose_name_plural,
                "app_name": self.model._meta.app_label,
                "model_name": self.model._meta.model_name,
            }
            if "site" in context:
                context["site"].update(opts)
            else:
                context.update({"site": opts})
        return context


class BaseListView(BaseSiteMixin, ListView):
    """Class base list"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objects = context.get("object_list")
        paginated = context.get("is_paginated")
        page = context.get("page_obj")
        paginator = context.get("paginator")
        opts = {
            "fields": self.get_list_fields(self.list_fields),
            "rows": self.get_rows(objects),
            "page_start_index": page.start_index() if paginated else 1,
            "page_end_index": page.end_index() if paginated else objects.count(),
            "total_records": paginator.count if paginated else objects.count(),
        }
        if hasattr(self, "bulk_fields") and self.bulk_fields is not None:
            opts.update({"bulks": self.get_list_fields(self.bulk_fields)})

        if "site" in context:
            context["site"].update(opts)
        else:
            context.update({"site": opts})

        return context

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get("paginate_by")
        if paginate_by:
            return paginate_by
        return super().get_paginate_by(queryset)

    def get_list_fields(self, list_fields):
        fields = [
            (name, Field.get_field_label(self.model, name)) for name in list_fields
        ]
        return fields

    def get_rows(self, queryset):
        rows = [
            {
                "instance": instance,
                "values": self.get_values(instance),
            }
            for instance in queryset
        ]
        return rows

    def get_values(self, instance):
        values = [Field.get_field_value(instance, name) for name in self.list_fields]
        return values


class BaseDetailView(BaseSiteMixin, DetailView):
    """Class base detail"""

    model = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        opts = {"results": self.get_results()}
        if "site" in context:
            context["site"].update(opts)
        else:
            context.update({"site": opts})

        return context

    def get_results(self):
        results = []
        for field in self.detail_fields:
            label = Field.get_field_label(self.object, field)
            value = Field.get_field_value(self.object, field)
            results.append({"cols": 12, "fields": [(label, value)]})
        return results


class BaseCreateView(BaseSiteMixin, CreateView):
    """Class Base creation"""

    model = None


class BaseUpdateView(BaseSiteMixin, UpdateView):
    """Class base the update"""

    model = None
