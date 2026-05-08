# 📒 Phonebook Application

A full-stack contact management system built with **FastAPI** (Python), **Vue 3**, and **PostgreSQL**, containerized with **Docker Compose**.

---

## 🛠 Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Frontend    | Vue 3 (Composition API) + Vite      |
| Backend     | FastAPI (Python 3.11) + SQLAlchemy  |
| Database    | PostgreSQL 15                       |
| Containers  | Docker + Docker Compose             |
| HTTP Client | Axios                               |

---

## 🚀 Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### Run with Docker Compose

```bash
# Clone the repository
git clone https://github.com/jainaidu866/Phonebook-Application.git
cd Phonebook-Application

# Start all services
docker-compose up --build
```

Once running, open:
- **Frontend**: http://localhost:8080
- **Backend API Docs (Swagger)**: http://localhost:8000/docs

---

## 🌱 Seed 50 Sample Contacts

After the app is running, in a separate terminal:

```bash
cd backend
pip install requests        # if not already installed
python seed_contacts.py     # seeds to http://localhost:8000 by default

# Or specify a custom API URL:
python seed_contacts.py --url http://localhost:8000
```

---

## 📡 API Endpoints

| Method | Endpoint           | Description                          |
|--------|--------------------|--------------------------------------|
| GET    | `/contacts`        | List all contacts (supports `?search=`) |
| POST   | `/contacts`        | Create a new contact                 |
| GET    | `/contacts/{id}`   | Get a contact by ID                  |
| PUT    | `/contacts/{id}`   | Update a contact by ID               |
| DELETE | `/contacts/{id}`   | Delete a contact by ID               |
| GET    | `/health`          | Health check                         |
| GET    | `/docs`            | Interactive Swagger UI               |

### Example: Create a Contact

```bash
curl -X POST http://localhost:8000/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "phone_number": "+1234567890",
    "email": "jane@example.com",
    "address": "123 Main St, Mumbai"
  }'
```

### Example: Search Contacts

```bash
curl "http://localhost:8000/contacts?search=jane"
```

---

## 🗄 Database Schema

```sql
contacts (
  id           SERIAL PRIMARY KEY,
  name         VARCHAR(255) NOT NULL,
  phone_number VARCHAR(50)  UNIQUE NOT NULL,
  email        VARCHAR(255) UNIQUE,
  address      TEXT,
  created_at   TIMESTAMP DEFAULT NOW()
)
```

---

## 🧪 Test with Postman / cURL

Import the Swagger spec from `http://localhost:8000/openapi.json` into Postman, or use the interactive docs at `/docs`.

---

## 📁 Project Structure

```
Phonebook-Application/
├── backend/
│   ├── main.py              # FastAPI app, models, routes
│   ├── requirements.txt
│   ├── seed_contacts.py     # Script to add 50 sample contacts
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.vue          # Main Vue component
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── .env
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Environment Variables

| Variable       | Default Value                                              | Description          |
|----------------|------------------------------------------------------------|----------------------|
| `DATABASE_URL` | `postgresql://phonebook_user:phonebook_pass@db:5432/phonebook_db` | Postgres connection  |
| `VITE_API_URL` | `http://localhost:8000`                                    | Backend API base URL |

---

## 🛑 Stopping the App

```bash
docker-compose down          # stop containers
docker-compose down -v       # stop containers + delete database volume
```