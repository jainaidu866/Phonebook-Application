📱 **Professional Phonebook Application**
A robust, full-stack contact management system engineered for high performance and reliability. This project demonstrates a modern microservices architecture, utilizing containerization to ensure seamless deployment and data persistence .  




🛠 **Tech Stack**
The application is built using a modern, scalable technology stack:

Frontend: Vue 3 (Composition API) with Vite for a fast, reactive user interface.  

Backend: FastAPI (Python) for asynchronous, high-concurrency RESTful API endpoints.  

Database: PostgreSQL 15 for reliable, relational data storage.  

Communication: Axios for standardized HTTP requests between the frontend and backend.  

Orchestration: Docker & Docker Compose for full-system containerization and networking.  




🚀 **Deployment and Installation**
Follow these steps to deploy the application in any environment:

1. Prerequisites
Ensure Docker Desktop is installed and running on your system. This eliminates the need to install local versions of Python or PostgreSQL.

2. System Initialization
Open your terminal in the project root directory and execute the following command:

Bash
docker-compose up --build
This command automatically builds the images, configures the internal network, and initializes the database schema .  




💻 **How to Use the Application**
Once the containers are active, you can interact with the system through the following access points:

Accessing the Web Interface
Navigate to http://localhost:8080 in your web browser.

Adding Contacts: Use the input header to enter a name and phone number. Click "Add Contact" to commit the entry to the PostgreSQL database.  
Viewing Contacts: The contact list automatically synchronizes with the database and displays all stored records in the data table.  
Managing Data: Each record includes a "Delete" option to permanently remove the entry from the system.  




**Interactive API Documentation**
Navigate to http://localhost:8000/docs to access the Swagger UI.

This provides a live environment to test all backend endpoints (GET, POST, DELETE) directly against the database .  




📁 **Project Architecture**
The repository is structured to maintain a clear separation of concerns:
/backend: Contains the FastAPI logic, SQLAlchemy ORM models, and database connection strings.  
/frontend: Contains the Vue 3 source code, including the reactive App.vue component and Vite configuration.  
docker-compose.yml: The central configuration file that manages service dependencies and environment variables .  




🛡️ **Key Features**

Data Persistence: Contacts remain securely stored in the PostgreSQL volume even after the application is shut down.  

Input Validation: The system enforces requirements for mandatory fields to ensure data quality.  

Containerized Networking: The frontend communicates securely with the backend via a dedicated Docker bridge network. 
