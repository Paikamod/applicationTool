import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
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

    for field in REQUIRED_FIELDS:
        if not data.get(field):
            # GEÄNDERT: statt ValueError -> JsonResponse mit Fehler
            # damit fetch() einen sauberen Response bekommt
            return JsonResponse({"success": False, "error": f"{field} is required"})

    # Leere Felder (z.B. address) aus data entfernen damit kein leerer String gespeichert wird
    data = {k: v for k, v in data.items() if v != ""}

    add_entry(**data)

    # GEÄNDERT: statt redirect -> JsonResponse
    # weil wir jetzt per fetch aufrufen und kein Redirect brauchen
    return JsonResponse({"success": True})


def open_all_view(request):
    status_open_all()

    # GEÄNDERT: statt redirect -> JsonResponse
    return JsonResponse({"success": True})


def delete_all_entries(request):
    delete_all()

    # GEÄNDERT: statt redirect -> JsonResponse
    return JsonResponse({"success": True})


def adzuna(request):
    jobtitle = request.GET.get("adzuna_jobtitle")
    location = request.GET.get("adzuna_location")

    jobs = []
    entries = list_entries()

    if jobtitle and location:
        jobs = adzuna_search(jobtitle, location)

        existing_entries = {
            (
                e.company_name.strip().lower(),
                e.jobtitle.strip().lower(),
            )
            for e in entries
        }

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
    if request.method == "POST":
        data = json.loads(request.body)

        add_entry(
            company_name=data.get("company_name"),
            address=data.get("address"),
            jobtitle=data.get("jobtitle"),
        )

        return JsonResponse({"success": True})


def entries_api(request):
    entries = list_entries()

    data = []

    for e in entries:
        data.append(
            {
                "id": e.id,
                "company_name": e.company_name,
                "address": e.address,
                "jobtitle": e.jobtitle,
                "status": e.status,
                "status_date": str(e.status_date),
            }
        )

    return JsonResponse({"entries": data})


def change_status_api(request):
    if request.method == "POST":
        data = json.loads(request.body)

        entry = Entry.objects.get(id=data["entry_id"])
        entry.status = data["status"]

        if data["status"] == "applied":
            entry.status_date = date.today()

        entry.save()

        return JsonResponse({"success": True})
