# Certification Exam Practice

This project is a practical exercise using **FastAPI** to develop a RESTful application dedicated to certification exam preparation. The application encompasses user management—covering registration, login, and deactivation—as well as handling certifications, exam questions, and exam attempts.

To facilitate the setup, **Docker** is utilized to orchestrate the services, including a **PostgreSQL** database that loads initial data from the `scripts` directory.

## Requirements

- Docker and Docker Compose installed.
- `make` installed on your system.

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/martinp95/certification_exam_practice.git
   cd certification_exam_practice
   ```

2. **Build the services:**
   ```bash
   make build
   ```

3. **Start the services:**
   ```bash
   make up
   ```
   This command starts all necessary Docker containers for the project.

4. **Stop the services:**
   ```bash
   make down
   ```

5. **Stop and remove containers and volumes**  
   (Useful for reinitializing the database and re-executing SQL scripts):
   ```bash
   make down-volumes
   ```

6. **Follow container logs in real time:**
   ```bash
   make logs
   ```

7. **Restart the services:**  
   (This command removes containers and volumes, then starts the services again):
   ```bash
   make restart
   ```

## Service Documentation Access

Each service exposes its API documentation via Swagger. Access the documentation at the following URL:

- **Service 1**: [http://localhost:<port>/docs](http://localhost:<port>/docs)  
  _Replace `<port>` with the appropriate port specified in `docker-compose.yml`._

## Postman Project

A Postman project is provided to facilitate API testing. Follow these steps to get started:

1. Import the [Postman collection](certification_exam_postman.json) located at the root of the project into your Postman application.
2. Configure the necessary environment variables in Postman, such as the base URLs and authentication tokens.
3. Execute the requests to test the various endpoints.

## Additional Notes

- Ensure that the ports specified in `docker-compose.yml` are not being used by other services on your machine.
- If you encounter any issues, check the container logs using:
  ```bash
  make logs
  ```

---
