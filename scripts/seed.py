from pymongo import MongoClient
import random

client = MongoClient("mongodb+srv://naveenamj2005_db_user:nIbYpiN0bGBmZseu@cluster0.brorwls.mongodb.net/?appName=Cluster0")
db = client["medrec_db"]

patients = [f"p{i}" for i in range(10, 21)]

sources = ["clinic_emr", "hospital", "patient_reported"]

medications_pool = [
    {"name": "aspirin", "dose": "100 mg"},
    {"name": "aspirin", "dose": "75 mg"},
    {"name": "lisinopril", "dose": "10 mg"},
    {"name": "losartan", "dose": "50 mg"},
    {"name": "metformin", "dose": "500 mg"}
]


def generate_med_list():
    return random.sample(medications_pool, k=random.randint(1, 3))


def seed_data():
    for patient in patients:
        for _ in range(random.randint(2, 3)):  # multiple snapshots

            record = {
                "patient_id": patient,
                "source": random.choice(sources),
                "medications": generate_med_list()
            }

            db.snapshots.insert_one(record)

    print("Seed data inserted successfully!")


if __name__ == "__main__":
    seed_data()