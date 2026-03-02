import json
from entries_old import entries


def save_entries(filename="entries.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(entries, file, indent=4, ensure_ascii=False)
    print(f"File saved as: '{filename}'")


def load_entries(filename="entries.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            entries.clear()
            entries.extend(data)
            print(f"File '{filename}' loaded.")
    except FileNotFoundError:
        entries.clear()
