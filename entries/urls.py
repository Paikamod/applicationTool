from django.urls import path
from .views import (
    entry_list,
    add_entry_by_form,
    open_all_view,
    delete_all_entries,
    adzuna,
    add_entry_by_adzuna,
)

urlpatterns = [
    path("", entry_list, name="entry_list"),
    path("newentry/", add_entry_by_form, name="add_entry_by_form"),
    path("openallview/", open_all_view, name="open_all_view"),
    path("deleteallentries/", delete_all_entries, name="delete_all_entries"),
    path("adzuna/", adzuna, name="adzuna"),
    path("addentrybyadzuna/", add_entry_by_adzuna, name="add_entry_by_adzuna"),
]
