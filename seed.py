import requests, random
API_URL = "http://localhost:8000/contacts"

def populate():
    names = ["Rahul", "Anjali", "Vikram", "Priya", "Amit", "Sonia", "Arjun", "Neha"]
    surnames = ["Sharma", "Verma", "Gupta", "Singh", "Patel", "Nair"]
    print(f"Connecting to {API_URL}...")
    for i in range(1, 51):
        payload = {
            "name": f"{random.choice(names)} {random.choice(surnames)}",
            "phone": f"+91{random.randint(7000000000, 9999999999)}",
            "email": f"user{i}@example.com",
            "address": f"Apartment {i}, Mumbai"
        }
        r = requests.post(API_URL, json=payload)
        print(f"Added {i}/50" if r.status_code in [200, 201] else f"Error {i}: {r.text}")

if __name__ == "__main__":
    populate()