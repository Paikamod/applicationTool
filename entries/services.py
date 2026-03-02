from datetime import date
from .models import Entry
import requests


def add_entry(**data):
    Entry.objects.create(**data)


"""def add_entry(company_name, jobtitle):
    if Entry.objects.filter(company_name=company_name, jobtitle=jobtitle).exists():
        print(f'Entry "{company_name}" - "{jobtitle}" already exists.')
        return None

    entry = Entry(
        company_name=company_name,
        jobtitle=jobtitle,
        status="open",
        status_date=date.today(),
    )
    entry.save()

    print(f'Entry "{company_name}" - "{jobtitle}" added.')
    return entry"""


def change_status(company_name, jobtitle, new_status):
    try:
        entry = Entry.objects.get(company_name=company_name, jobtitle=jobtitle)
    except Entry.DoesNotExist:
        print("No entry found.")
        return

    if new_status == "applied":
        entry.status_date = date.today()
    entry.status = new_status
    entry.save()

    # print(f'Status updated for "{company_name}" - "{jobtitle}".')


def delete_entry(company_name, jobtitle):
    deleted, _ = Entry.objects.filter(
        company_name=company_name, jobtitle=jobtitle
    ).delete()

    if deleted:
        print(f'Entry "{company_name}" - {jobtitle} deleted.')
    else:
        print("No entry for deletion found")


def list_entries(status=None):
    qs = Entry.objects.all()

    if status:
        qs = qs.filter(status=status)

    return qs


def status_open_all():
    for e in list_entries():
        c = e.company_name
        t = e.jobtitle
        s = e.status
        if s != "open":
            ns = "open"
            change_status(c, t, ns)
            print(f"Status of {c} - {t} changed to open.")


def delete_all():
    for e in list_entries():
        c = e.company_name
        t = e.jobtitle
        delete_entry(c, t)


def adzuna_search(keyword, location):
    url = f"https://api.adzuna.com/v1/api/jobs/de/search/1"
    params = {
        "app_id": "",
        "app_key": "",
        "results_per_page": 100,
        "what": keyword,
        "where": location,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])

    return []
