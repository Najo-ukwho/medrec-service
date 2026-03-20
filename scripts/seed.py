from pymongo import MongoClient
from datetime import datetime
import random

client = MongoClient("mongodb+srv://naveenamj2005_db_user:nIbYpiN0bGBmZseu@cluster0.brorwls.mongodb.net/?appName=Cluster0")
db = client["medrec_db"]

patients = [f"p{i}" for i in range(1, 21)]

sources = ["clinic_emr", "hospital", "patient_reported"]

medications_pool = [
    {"name": "aspirin", "dose": "100 mg"},
    {"name": "aspirin", "dose": "75 mg"},
    {"name": "lisinopril", "dose": "10 mg"},
    {"name": "losartan", "dose": "50 mg"},
    {"name": "metformin", "dose": "500 mg"}
]


def generate_med_list():
    return random.sample(medications_pool, k=random.randint(1, 2))


def seed_data():
    for patient in patients:

        for _ in range(random.randint(2, 3)):

            existing_count = db.snapshots.count_documents({"patient_id": patient})

            record = {
                "patient_id": patient,
                "source": random.choice(sources),
                "clinic_id": random.choice(["clinic_A", "clinic_B"]),  # ✅ NEW
                "medications": generate_med_list(),
                "version": existing_count + 1,
                "created_at": datetime.utcnow()
            }

            db.snapshots.insert_one(record)

    print("Seed data inserted successfully!")


if __name__ == "__main__":
    seed_data()