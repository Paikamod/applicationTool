from datetime import date

ALLOWED_STATUS = {"open", "applied", "rejected"}
entries = []


def add_entry(company_name, jobtitle):
    for entry in entries:
        if entry["company_name"] == company_name and entry["jobtitle"] == jobtitle:
            print(f"'{company_name}' - '{jobtitle}' already exists.")
            return

    new_entry = {
        "company_name": company_name,
        "jobtitle": jobtitle,
        "status": "open",
        "status_date": date.today().isoformat(),
    }

    entries.append(new_entry)
    print(f"Entry '{company_name}' - '{jobtitle}' added.")


def change_status(company_name, jobtitle, new_status):
    if new_status not in ALLOWED_STATUS:
        raise ValueError(f"Ungültiger Status: '{new_status}'")

    for entry in entries:
        if entry["company_name"] == company_name and entry["jobtitle"] == jobtitle:
            entry["status"] = new_status
            entry["status_date"] = date.today().isoformat()
            print(
                f"Status for '{company_name}' - '{jobtitle}' changed to: '{new_status}'"
            )
            return

    print("Kein passender Eintrag gefunden.")


def delete_entry(company_name, jobtitle):
    for index, entry in enumerate(entries):
        if entry["company_name"] == company_name and entry["jobtitle"] == jobtitle:
            del entries[index]
            print(f"Entry '{company_name}' - '{jobtitle}' deleted.")
            return

    print("Kein passender Eintrag gefunden.")
