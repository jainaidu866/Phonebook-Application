# 📒 Phonebook Application

A full-stack contact management system built with **FastAPI**, **Vue 3**, **PostgreSQL**, and **Docker**.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 (Composition API) + Vite |
| Backend | FastAPI (Python) |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy |
| HTTP Client | Axios |
| Containerization | Docker + Docker Compose |

---

## 📁 Project Structure

```
Phonebook-Application/
│
├── backend/
│   ├── main.py          # FastAPI app — all routes, models, schemas
│   ├── seed.py          # Script to add 50 sample contacts
│   ├── requirements.txt # Python dependencies
│   ├── Dockerfile       # Backend container config
│   └── dist/            # Built Vue frontend (served by FastAPI)
│
├── frontend/
│   ├── src/
│   │   ├── App.vue      # Main Vue component (entire UI)
│   │   └── main.js      # Vue app entry point
│   ├── .env             # API URL config (VITE_API_URL)
│   ├── package.json     # Node dependencies
│   └── Dockerfile       # Frontend container config
│
├── Docker-compose.yml   # Defines all 3 services
└── README.md
```

---

## 🗄 Database Schema

Table name: `contacts`

| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key, auto increment |
| name | String(255) | Required |
| phone_number | String(50) | Required, unique (e.g. +911234567890) |
| email | String(255) | Optional, unique |
| address | Text | Optional |
| created_at | DateTime | Auto set to current time |

---

## 🚀 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /contacts | Get all contacts (supports search + pagination) |
| POST | /contacts | Add a new contact |
| GET | /contacts/{id} | Get a specific contact |
| PUT | /contacts/{id} | Update a specific contact |
| DELETE | /contacts/{id} | Delete a specific contact |
| GET | /health | Health check |

### Pagination parameters for GET /contacts

| Param | Default | Description |
|-------|---------|-------------|
| skip | 0 | How many records to skip |
| limit | 9 | How many records to return |
| search | - | Filter by name or phone number |

**Response format:**
```json
{
  "total": 51,
  "items": [ ...contacts... ]
}
```

---

## ⚙️ Setup and Installation

### Prerequisites

Make sure you have these installed:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — **required**
- [Node.js](https://nodejs.org/) — for building the frontend
- [ngrok](https://ngrok.com/) — only needed if sharing with others

---

## 💻 Running Locally

### Step 1 — Clone the repo
```bash
git clone https://github.com/jainaidu866/Phonebook-Application.git
cd Phonebook-Application
```

### Step 2 — Build the frontend
```bash
cd frontend
npm install
npm run build
```

### Step 3 — Copy built frontend into backend
```bash
# Windows
xcopy /E /I dist ..\backend\dist

# Mac / Linux
cp -r dist ../backend/dist
```

### Step 4 — Start all containers
```bash
cd ..
docker-compose up --build
```

### Step 5 — Open the app
Go to: **http://localhost:8000**

The app will load directly. API docs are at: **http://localhost:8000/docs**

---

## 🌱 Adding Sample Data (50 Contacts)

To populate the database with 50 sample contacts, run the seed script inside the backend container:

```bash
docker exec -it phonebook-backend python seed.py
```

This inserts 50 realistic contacts with names, phone numbers, emails, and addresses.

---

## 🌐 Sharing with Others via ngrok

Use this when you want to share the app with someone outside your network (e.g. a recruiter).

### Step 1 — Install and authenticate ngrok (one time only)
```bash
ngrok config add-authtoken YOUR_TOKEN_HERE
```
Get your token from: https://dashboard.ngrok.com/get-started/your-authtoken

### Step 2 — Start the app
```bash
docker-compose up --build
```

### Step 3 — Start ngrok tunnel
```bash
ngrok http 8000
```

You will see a URL like: `https://abc123.ngrok-free.app`

### Step 4 — Update frontend/.env
```
VITE_API_URL=https://abc123.ngrok-free.app
```

### Step 5 — Rebuild frontend and copy dist
```bash
cd frontend
npm run build
xcopy /E /I dist ..\backend\dist   # Windows
cd ..
docker-compose up --build
```

### Step 6 — Share the ngrok URL
Send `https://abc123.ngrok-free.app` to the recruiter. That single URL opens the full app.

> **Note:** ngrok URLs change every time you restart ngrok. Repeat steps 3–6 each time.

---

## ✨ Features

- **Add contacts** — name, phone, email, address via modal form
- **Edit contacts** — pre-filled edit form, saves changes instantly
- **Delete contacts** — confirmation dialog before deleting
- **Search** — live search by name or phone number
- **Pagination** — 9 contacts per page with page controls
- **Input validation** — name required, phone format checked (+digits), email format checked
- **Duplicate detection** — prevents duplicate phone numbers and emails
- **Color avatars** — each contact gets a unique color based on their name
- **Toast notifications** — success/error messages after every action
- **Responsive** — works on mobile and desktop

---

## 🔧 Environment Variables

### backend
| Variable | Default | Description |
|----------|---------|-------------|
| DATABASE_URL | postgresql://phonebook_user:phonebook_pass@db:5432/phonebook_db | PostgreSQL connection string |

### frontend
| Variable | Description |
|----------|-------------|
| VITE_API_URL | Backend API URL (use ngrok URL when sharing externally) |

---

## 🧪 Testing the API

Once running, open **http://localhost:8000/docs** for the interactive Swagger UI where you can test all endpoints directly in the browser.

Example — add a contact using curl:
```bash
curl -X POST http://localhost:8000/contacts \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "phone_number": "+911234567890", "email": "john@example.com"}'
```

---

## 🐳 Docker Services

| Service | Port | Description |
|---------|------|-------------|
| backend | 8000 | FastAPI app + serves Vue frontend |
| db | 5432 | PostgreSQL database |
| frontend | 8080 | Vue dev server (development only) |

All services communicate through Docker's internal bridge network. The database is not exposed publicly.

---

## 📝 Notes

- Database data **persists** even after stopping containers (Docker volume)
- To completely reset the database: `docker-compose down -v` then `docker-compose up --build`
- The frontend is served directly by FastAPI in production (from the `dist` folder), so only one port (8000) is needed