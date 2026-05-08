#!/usr/bin/env python3
"""
seed_contacts.py — Adds 50 sample contacts to the Phonebook API.
Usage: python seed_contacts.py [--url http://localhost:8000]
"""

import requests
import argparse
import sys

CONTACTS = [
    {"name": "Aarav Sharma",      "phone_number": "+911234567801", "email": "aarav.sharma@email.com",      "address": "12 MG Road, Mumbai, Maharashtra"},
    {"name": "Priya Patel",       "phone_number": "+911234567802", "email": "priya.patel@email.com",       "address": "45 Linking Road, Bandra, Mumbai"},
    {"name": "Rohan Mehta",       "phone_number": "+911234567803", "email": "rohan.mehta@email.com",       "address": "8 Park Street, Kolkata, West Bengal"},
    {"name": "Ananya Gupta",      "phone_number": "+911234567804", "email": "ananya.gupta@email.com",      "address": "22 Connaught Place, New Delhi"},
    {"name": "Vikram Singh",      "phone_number": "+911234567805", "email": "vikram.singh@email.com",      "address": "67 Brigade Road, Bangalore, Karnataka"},
    {"name": "Kavya Nair",        "phone_number": "+911234567806", "email": "kavya.nair@email.com",        "address": "3 Marine Drive, Kochi, Kerala"},
    {"name": "Arjun Reddy",       "phone_number": "+911234567807", "email": "arjun.reddy@email.com",       "address": "15 Banjara Hills, Hyderabad, Telangana"},
    {"name": "Sneha Joshi",       "phone_number": "+911234567808", "email": "sneha.joshi@email.com",       "address": "29 FC Road, Pune, Maharashtra"},
    {"name": "Karan Malhotra",    "phone_number": "+911234567809", "email": "karan.malhotra@email.com",    "address": "54 Sector 17, Chandigarh"},
    {"name": "Meera Iyer",        "phone_number": "+911234567810", "email": "meera.iyer@email.com",        "address": "11 Anna Salai, Chennai, Tamil Nadu"},
    {"name": "Rahul Verma",       "phone_number": "+911234567811", "email": "rahul.verma@email.com",       "address": "38 Hazratganj, Lucknow, UP"},
    {"name": "Pooja Yadav",       "phone_number": "+911234567812", "email": "pooja.yadav@email.com",       "address": "7 Civil Lines, Nagpur, Maharashtra"},
    {"name": "Aditya Kumar",      "phone_number": "+911234567813", "email": "aditya.kumar@email.com",      "address": "19 Elliot's Beach, Chennai"},
    {"name": "Divya Pillai",      "phone_number": "+911234567814", "email": "divya.pillai@email.com",      "address": "63 Kaloor, Kochi, Kerala"},
    {"name": "Siddharth Rao",     "phone_number": "+911234567815", "email": "siddharth.rao@email.com",     "address": "41 Koramangala, Bangalore"},
    {"name": "Tanvi Shah",        "phone_number": "+911234567816", "email": "tanvi.shah@email.com",        "address": "2 Navrangpura, Ahmedabad, Gujarat"},
    {"name": "Nikhil Desai",      "phone_number": "+911234567817", "email": "nikhil.desai@email.com",      "address": "88 Dadar, Mumbai, Maharashtra"},
    {"name": "Ayesha Khan",       "phone_number": "+911234567818", "email": "ayesha.khan@email.com",       "address": "31 Lal Bagh, Lucknow, UP"},
    {"name": "Ravi Krishnan",     "phone_number": "+911234567819", "email": "ravi.krishnan@email.com",     "address": "74 T Nagar, Chennai, Tamil Nadu"},
    {"name": "Lakshmi Menon",     "phone_number": "+911234567820", "email": "lakshmi.menon@email.com",     "address": "5 Trivandrum Road, Kochi"},
    {"name": "Amit Tiwari",       "phone_number": "+911234567821", "email": "amit.tiwari@email.com",       "address": "23 Gomti Nagar, Lucknow"},
    {"name": "Shreya Bansal",     "phone_number": "+911234567822", "email": "shreya.bansal@email.com",     "address": "9 Vasant Vihar, New Delhi"},
    {"name": "Manish Saxena",     "phone_number": "+911234567823", "email": "manish.saxena@email.com",     "address": "47 Civil Lines, Allahabad, UP"},
    {"name": "Nisha Agarwal",     "phone_number": "+911234567824", "email": "nisha.agarwal@email.com",     "address": "16 Rajpur Road, Dehradun, Uttarakhand"},
    {"name": "Suresh Babu",       "phone_number": "+911234567825", "email": "suresh.babu@email.com",       "address": "33 Adyar, Chennai, Tamil Nadu"},
    {"name": "Deepika Chawla",    "phone_number": "+911234567826", "email": "deepika.chawla@email.com",    "address": "61 Karol Bagh, New Delhi"},
    {"name": "Rajesh Khanna",     "phone_number": "+911234567827", "email": "rajesh.khanna@email.com",     "address": "14 Salt Lake, Kolkata"},
    {"name": "Preeti Srivastava", "phone_number": "+911234567828", "email": "preeti.srivastava@email.com", "address": "27 Mahanagar, Lucknow"},
    {"name": "Gaurav Mishra",     "phone_number": "+911234567829", "email": "gaurav.mishra@email.com",     "address": "52 New Palasia, Indore, MP"},
    {"name": "Swati Pandey",      "phone_number": "+911234567830", "email": "swati.pandey@email.com",      "address": "6 Sigra, Varanasi, UP"},
    {"name": "Harsh Vardhan",     "phone_number": "+911234567831", "email": "harsh.vardhan@email.com",     "address": "18 Sector 62, Noida, UP"},
    {"name": "Anjali Dubey",      "phone_number": "+911234567832", "email": "anjali.dubey@email.com",      "address": "43 Scindia House, Gwalior, MP"},
    {"name": "Varun Kapoor",      "phone_number": "+911234567833", "email": "varun.kapoor@email.com",      "address": "79 Rajinder Nagar, New Delhi"},
    {"name": "Simran Gill",       "phone_number": "+911234567834", "email": "simran.gill@email.com",       "address": "25 Model Town, Ludhiana, Punjab"},
    {"name": "Mohit Arora",       "phone_number": "+911234567835", "email": "mohit.arora@email.com",       "address": "37 Patel Nagar, Amritsar, Punjab"},
    {"name": "Rohini Shukla",     "phone_number": "+911234567836", "email": "rohini.shukla@email.com",     "address": "11 Napier Town, Jabalpur, MP"},
    {"name": "Sanjay Bose",       "phone_number": "+911234567837", "email": "sanjay.bose@email.com",       "address": "58 Alipore, Kolkata, WB"},
    {"name": "Pallavi Jain",      "phone_number": "+911234567838", "email": "pallavi.jain@email.com",      "address": "4 Tilak Nagar, Jaipur, Rajasthan"},
    {"name": "Abhishek Tomar",    "phone_number": "+911234567839", "email": "abhishek.tomar@email.com",    "address": "66 Agra Road, Mathura, UP"},
    {"name": "Rekha Bhatt",       "phone_number": "+911234567840", "email": "rekha.bhatt@email.com",       "address": "20 Moti Bagh, New Delhi"},
    {"name": "Sunil Chauhan",     "phone_number": "+911234567841", "email": "sunil.chauhan@email.com",     "address": "34 Jakhan, Dehradun, Uttarakhand"},
    {"name": "Archana Kulkarni",  "phone_number": "+911234567842", "email": "archana.kulkarni@email.com",  "address": "72 Deccan Gymkhana, Pune"},
    {"name": "Piyush Tripathi",   "phone_number": "+911234567843", "email": "piyush.tripathi@email.com",   "address": "48 Lanka, Varanasi, UP"},
    {"name": "Ishita Chatterjee", "phone_number": "+911234567844", "email": "ishita.chatterjee@email.com", "address": "13 Dhakuria, Kolkata"},
    {"name": "Tarun Malviya",     "phone_number": "+911234567845", "email": "tarun.malviya@email.com",     "address": "55 Sudama Nagar, Indore, MP"},
    {"name": "Kriti Bhardwaj",    "phone_number": "+911234567846", "email": "kriti.bhardwaj@email.com",    "address": "28 Green Park, New Delhi"},
    {"name": "Sachin Lokhande",   "phone_number": "+911234567847", "email": "sachin.lokhande@email.com",   "address": "83 Pimpri, Pune, Maharashtra"},
    {"name": "Vandana Tiwari",    "phone_number": "+911234567848", "email": "vandana.tiwari@email.com",    "address": "39 Bhawarkua, Indore, MP"},
    {"name": "Nitin Rawat",       "phone_number": "+911234567849", "email": "nitin.rawat@email.com",       "address": "17 Saket, New Delhi"},
    {"name": "Geeta Krishnamurti","phone_number": "+911234567850", "email": "geeta.krishnamurti@email.com","address": "92 Adambakkam, Chennai, TN"},
]

def seed(base_url: str):
    url = f"{base_url}/contacts"
    added, skipped, failed = 0, 0, 0

    print(f"\n🌱  Seeding 50 contacts to {url}\n{'─'*50}")

    for contact in CONTACTS:
        try:
            res = requests.post(url, json=contact, timeout=10)
            if res.status_code == 201:
                print(f"  ✅  Added   → {contact['name']}")
                added += 1
            elif res.status_code == 409:
                print(f"  ⚠️   Exists  → {contact['name']}")
                skipped += 1
            else:
                print(f"  ❌  Failed  → {contact['name']}  [{res.status_code}] {res.text}")
                failed += 1
        except requests.ConnectionError:
            print(f"\n❌  Cannot connect to {base_url}. Is the server running?")
            sys.exit(1)

    print(f"\n{'─'*50}")
    print(f"✅  Added: {added}   ⚠️  Already existed: {skipped}   ❌ Failed: {failed}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed 50 contacts into the Phonebook API")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the API")
    args = parser.parse_args()
    seed(args.url.rstrip("/"))