# 🧩 TaskFlow API

TaskFlow is a **FastAPI-based backend** designed to manage projects, tasks, and team collaboration.  
It’s a practical learning project built to help understand **FastAPI**, **SQLAlchemy**, **Pydantic**, and **clean backend architecture** — all while connecting to a real **MySQL database**.

---

## 🚀 Overview

TaskFlow lets users:
- Register and log in with **JWT-based authentication**
- Create and manage **projects**
- Assign **tasks** within projects
- Track progress and collaboration between users
- Manage roles and access in a secure, well-structured API environment

---

## 🎯 Learning Objectives

This project is not just about making an API — it’s about learning to build a **scalable backend** that feels production-ready.

You’ll learn:
- Proper **FastAPI folder structure**
- **Type-safe** code using Pydantic
- How to use **SQLAlchemy ORM** effectively with MySQL
- **Dependency Injection** for clean, testable code
- How to configure **CORS** and **middlewares**
- Writing docstrings that auto-generate clear `/docs` and `/redoc` documentation
- Handling **authentication and token-based authorization** using JWT

---

## ⚙️ Configuration

The app’s behavior is managed through environment variables in a `.env` file.

Example:
```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/taskflow_db
PROJECT_NAME=TaskFlow API
PROJECT_DESCRIPTION=An API for managing projects, tasks, and team collaboration.
PROJECT_VERSION=1.0.0
BASE_PATH=/api/v1
````

The above values are read through `pydantic.BaseSettings` in `config.py`, which allows you to easily manage configurations without hardcoding.

---

## 🧠 API Meta Configuration

In FastAPI, you can define API metadata inside your main application initialization.
Example:

```python
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.BASE_PATH}/openapi.json",
    docs_url=f"{settings.BASE_PATH}/docs",
    redoc_url=f"{settings.BASE_PATH}/redoc",
)
```

This gives your API:

* A **base path** (e.g., `/api/v1`)
* Custom titles, descriptions, and version numbers in Swagger
* Organized documentation URLs

---

## 🧩 Tech Stack

| Component       | Purpose                         |
| --------------- | ------------------------------- |
| **FastAPI**     | Web framework for building APIs |
| **SQLAlchemy**  | ORM for database operations     |
| **Pydantic**    | Data validation and type safety |
| **PyMySQL**     | MySQL driver                    |
| **Alembic**     | Database migrations             |
| **JWT (PyJWT)** | Authentication                  |
| **Uvicorn**     | ASGI server for running FastAPI |

---

## 🧰 Key Features (Coming as You Build)

* User registration and login
* JWT authentication and refresh tokens
* CRUD operations for Projects and Tasks
* Role-based access (owner, collaborator)
* CORS and Middleware setup
* Clean dependency injection for database sessions
* Organized service layer and business logic separation
* Structured and well-documented API endpoints

---

## 📚 Documentation

After running the server (`uvicorn app.main:app --reload`):

* Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Development Notes

* Migrations are handled with **Alembic**.
* Database sessions are managed using FastAPI’s dependency injection.
* All routes are versioned under `/api/v1`.
* The service layer (`/services`) separates logic from route handling.
* Environment variables are loaded dynamically using `python-dotenv`.

---

## 💡 Purpose

TaskFlow is not meant to be a finished product — it’s a **learning sandbox** for mastering backend concepts with FastAPI.
You’ll gradually evolve it into a structured, production-style API with full authentication, data persistence, and clarity in documentation.

---

## 🔒 License

MIT License © 2025 Arya Danech
