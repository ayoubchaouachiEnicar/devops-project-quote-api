# DevOps Project - Quote API

A Flask-based REST API for managing quotes with complete DevOps implementation including CI/CD pipeline, containerization, and security scanning.

## 📋 Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Docker](#docker)
- [API Endpoints](#api-endpoints)
- [Security Scanning](#security-scanning)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring & Observability](#monitoring--observability)

## ✨ Features

- **RESTful API** for managing quotes (CRUD operations)
- **Containerized** with Docker
- **CI/CD Pipeline** using GitHub Actions
- **Security Scanning** with Bandit (SAST) and OWASP ZAP (DAST)
- **Observability** with OpenTelemetry and Jaeger tracing
- **Structured Logging** with Python structlog
- **Health Check** endpoint for monitoring
- **Automated Testing** in CI pipeline

## 🛠 Technologies

- **Backend**: Python 3.12, Flask
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Security**: Bandit, OWASP ZAP
- **Monitoring**: OpenTelemetry, Jaeger
- **Registry**: Docker Hub

## 📦 Prerequisites

- Python 3.12+
- Docker
- Git

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/ayoubchaouachiEnicar/devops-project-quote-api.git
cd devops-project-quote-api
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🏃 Running the Application

### Locally (without Docker)

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### With Docker

#### Build the image

```bash
docker build -t todo-api .
```

#### Run the container

```bash
docker run -p 5000:5000 --name todo-api-container todo-api
```

### Using Docker Compose

```bash
docker-compose up
```

## 🐳 Docker

### Pull from Docker Hub

```bash
docker pull sobergragos/todo-api:latest
docker run -p 5000:5000 sobergragos/todo-api:latest
```

### Docker Hub Repository

[sobergragos/todo-api](https://hub.docker.com/r/sobergragos/todo-api)

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check endpoint |
| GET | `/todos` | Get all todos |
| GET | `/todos/<id>` | Get a specific todo |
| POST | `/todos` | Create a new todo |
| PUT | `/todos/<id>` | Update a todo |
| DELETE | `/todos/<id>` | Delete a todo |

### Example Usage

#### Create a Todo

```bash
curl -X POST http://localhost:5000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn DevOps", "completed": false}'
```

#### Get All Todos

```bash
curl http://localhost:5000/todos
```

#### Update a Todo

```bash
curl -X PUT http://localhost:5000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn DevOps", "completed": true}'
```

#### Delete a Todo

```bash
curl -X DELETE http://localhost:5000/todos/1
```

## 🔒 Security Scanning

### SAST (Static Application Security Testing)

**Bandit** is used for Python code security scanning.

```bash
# Install Bandit
pip install bandit

# Run scan
bandit -r . -f txt -o bandit-report.txt

# Or for detailed output
bandit -r app.py
```

### DAST (Dynamic Application Security Testing)

**OWASP ZAP** is used for runtime security testing.

```bash
# Make sure the app is running first
python app.py

# Run ZAP baseline scan (in another terminal)
docker run -v $(pwd):/zap/wrk:rw -t zaproxy/zap-stable \
  zap-baseline.py -t http://host.docker.internal:5000 \
  -r zap-baseline-report.html --auto
```

## 🔄 CI/CD Pipeline

The project uses **GitHub Actions** for automated CI/CD.

### Pipeline Stages

1. **Checkout Code** - Pull the latest code
2. **Setup Python** - Configure Python 3.12 environment
3. **Install Dependencies** - Install required packages
4. **SAST Scan** - Run Bandit security scan
5. **Build Docker Image** - Create Docker image
6. **Login to Docker Hub** - Authenticate with Docker Hub
7. **Push to Docker Hub** - Publish the image

### Trigger

The pipeline runs automatically on:
- Push to `main` branch
- Pull requests to `main` branch

### Required Secrets

Set these in GitHub repository settings (Settings → Secrets and variables → Actions):

- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Docker Hub access token with read/write permissions

## 📊 Monitoring & Observability

### OpenTelemetry Tracing

The application is instrumented with OpenTelemetry and sends traces to Jaeger.

#### Start Jaeger (optional)

```bash
docker run -d --name jaeger \
  -p 6831:6831/udp \
  -p 16686:16686 \
  jaegertracing/all-in-one:latest
```

Access Jaeger UI at `http://localhost:16686`

### Structured Logging

The application uses `structlog` for structured JSON logging, making it easier to parse and analyze logs.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Project Structure

```
devops-project-quote-api/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions workflow
├── app.py                     # Main Flask application
├── Dockerfile                 # Docker configuration
├── requirements.txt           # Python dependencies
├── bandit-report.txt          # SAST security scan results
├── zap-baseline-report.html   # DAST security scan results
└── README.md                  # This file
```

## 📄 License

This project is part of a DevOps educational assignment.

## 👨‍💻 Author

**Ayoub Chaouachi**
- GitHub: [@ayoubchaouachiEnicar](https://github.com/ayoubchaouachiEnicar)
- Docker Hub: [sobergragos](https://hub.docker.com/u/sobergragos)

---

**Built with ❤️ for DevOps learning**