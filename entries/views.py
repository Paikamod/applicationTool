from django.shortcuts import render, redirect
from .services import (
    list_entries,
    add_entry,
    status_open_all,
    delete_all,
    adzuna_search,
)
from .models import Entry
from datetime import date


def entry_list(request):
    if request.method == "POST":
        entry_id = request.POST.get("entry_id")
        new_status = request.POST.get("status")

        entry = Entry.objects.get(id=entry_id)
        entry.status = new_status
        if new_status == "applied":
            entry.status_date = date.today()
        entry.save()

        return redirect("entry_list")

    entries = list_entries()
    return render(request, "entries/entry_list.html", {"entries": entries})


def add_entry_by_form(request):
    REQUIRED_FIELDS = ["company_name", "jobtitle"]

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken", None)

    print(data)

    for field in REQUIRED_FIELDS:
        if not data.get(field):
            raise ValueError(f"{field} is required")

    """for key, value in data.items():
        if value == "":
            data[key] = "X"""

    add_entry(**data)

    return redirect("entry_list")


def open_all_view(request):
    status_open_all()

    return redirect("entry_list")


def delete_all_entries(request):
    delete_all()

    return redirect("entry_list")


def adzuna(request):
    jobtitle = request.GET.get("adzuna_jobtitle")
    location = request.GET.get("adzuna_location")

    jobs = []
    entries = list_entries()  # Nur EIN Query

    if jobtitle and location:
        jobs = adzuna_search(jobtitle, location)

        # 🔹 Bestehende Einträge normalisiert vorbereiten
        existing_entries = {
            (
                e.company_name.strip().lower(),
                e.jobtitle.strip().lower(),
            )
            for e in entries
        }

        # 🔹 Jobs markieren
        for job in jobs:
            company = job.get("company", {}).get("display_name", "")
            title = job.get("title", "")

            key = (
                company.strip().lower(),
                title.strip().lower(),
            )

            job["already_added"] = key in existing_entries

    return render(
        request,
        "entries/entry_list.html",
        {
            "entries": entries,
            "jobs": jobs,
        },
    )


def add_entry_by_adzuna(request):
    REQUIRED_FIELDS = ["company_name", "jobtitle"]

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken", None)

    job_search = data.pop("adzuna_jobtitle", None)
    location_search = data.pop("adzuna_location", None)

    for field in REQUIRED_FIELDS:
        if not data.get(field):
            raise ValueError(f"{field} is required")

    """for key, value in data.items():
        if value == "":
            data[key] = "X"""

    add_entry(**data)

    jobtitle = request.POST.get("adzuna_jobtitle")
    location = request.POST.get("adzuna_location")

    return redirect(
        f"/entries/adzuna/?adzuna_jobtitle={job_search}&adzuna_location={location_search}"
    )
