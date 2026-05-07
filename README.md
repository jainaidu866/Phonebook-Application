📱 **Professional Phonebook Application**
A robust, full-stack contact management system engineered for high performance and reliability. This project demonstrates a modern microservices architecture, utilizing containerization to ensure seamless deployment and data persistence .  


🖼️ **User Interface**
The modern, responsive interface allows for seamless contact management across all devices.
[Final UserInterface Screenshot](<Phonebook UI.jpeg>)

🛠 **Tech Stack**
The application is built using a modern, scalable technology stack:Frontend: Vue 3 (Composition API) with Vite for a fast, reactive user interface.  Backend: FastAPI (Python) for asynchronous, high-concurrency RESTful API endpoints.  Database: PostgreSQL 15 for reliable, relational data storage.  Communication: Axios for standardized HTTP requests between the frontend and backend.  Orchestration: Docker & Docker Compose for full-system containerization and networking.  


🚀 **Deployment and Installation**
Follow these steps to deploy the application in any environment:
1. PrerequisitesEnsure Docker Desktop is installed and running on your system. This eliminates the need to install local versions of Python or PostgreSQL.  
2. System InitializationOpen your terminal in the project root directory and execute the following command:Bashdocker-compose up --build

This command automatically builds the images, configures the internal network, and initializes the database schema.  

💻 **How to Use the Application**
Once the containers are active, you can interact with the system through the following access points:Accessing the Web InterfaceNavigate to **http://localhost:8080** in your web browser.

**Adding Contacts**: Use the input header to enter a name and phone number. Click "Add Contact" to commit the entry to the PostgreSQL database.  
**Viewing Contacts**: The contact list automatically synchronizes with the database and displays all stored records in the data table.  Editing/Updating: Click the "Edit" button to modify existing contact details via a secure modal.  
**Managing Data**: Each record includes a "Delete" option to permanently remove the entry from the system.  Interactive API DocumentationNavigate to http://localhost:8000/docs to access the Swagger UI. This provides a live environment to test all backend endpoints (GET, POST, PUT, DELETE) directly against the database.  

🧪 **Testing the Application**
To verify the system functionality as per requirements:  Automated Validation: Attempt to add a contact with an invalid phone format; the system will trigger a validation error.  
API Testing: Use the Swagger UI at the link above to execute test cases for each RESTful endpoint.Persistence Test: Stop the containers and restart them; verify that previously added contacts remain available in the list.

📁 **Project Architecture**

/**backend**: Contains the FastAPI logic, SQLAlchemy ORM models, and database connection strings.  

/**frontend**: Contains the Vue 3 source code, including the reactive App.vue component and Vite configuration.  

**docker-compose.yml**: The central configuration file that manages service dependencies and environment variables.  

🛡️ **Key Features Data Persistence:** 
Contacts remain securely stored in the PostgreSQL volume even after the application is shut down.Input Validation: The system enforces requirements for mandatory fields and specific phone formats to ensure data quality.  Containerized Networking: The frontend communicates securely with the backend via a dedicated Docker bridge network.  
