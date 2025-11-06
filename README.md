# Django REST API Project

This project is a backend REST API developed using **Django** and **Django REST Framework**.  
It allows clients to perform CRUD (Create, Read, Update, Delete) operations over HTTP and returns data in JSON format.

---

## 🚀 Features

- RESTful API architecture
- CRUD operations supported
- JSON request and response format
- Uses Django ORM for database operations
- Can be connected to a frontend or used as a standalone backend

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python    | Programming Language |
| Django    | Web Framework |
| Django REST Framework | API Handling |
| SQLite | Database |

---

## 📦 Project Setup

### 1. Clone the Repository
git clone https://github.com/saikiran419/REST_API.git
cd REST_API

2. Create a virtual environment
python3 -m venv env
source env/bin/activate   # Mac/Linux
env\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Apply migrations
python manage.py migrate

5. Run the server
   python manage.py runserve

6.Server runs at:
http://127.0.0.1:8000/



