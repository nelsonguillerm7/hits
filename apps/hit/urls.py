"""Auth models."""

# Django
from django.urls import path

# Views
from apps.hit.views import (
    HitsListView,
    HitsDetailView,
    HitsCreateView,
    HitsUpdateView,
    HitBulkUpdateView,
)

app_name = "hit"

urlpatterns = (
    path(route="hits/", view=HitsListView.as_view(), name="hits_list"),
    path(route="hits/<int:pk>/", view=HitsDetailView.as_view(), name="hits_detail"),
    path(
        route="hits/<int:pk>/update/", view=HitsUpdateView.as_view(), name="hits_update"
    ),
    path(route="hits/create/", view=HitsCreateView.as_view(), name="hits_create"),
    path(route="hits/bulk/", view=HitBulkUpdateView.as_view(), name="hits_bulk"),
)
