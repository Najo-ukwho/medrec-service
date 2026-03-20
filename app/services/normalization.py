def normalize_medication(med):
    return {
        "name": med["name"].strip().lower(),
        "dose": med["dose"].strip().lower(),
        "status": med.get("status", "active")
    }