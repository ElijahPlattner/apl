# APL Project — React + Django Setup

## 🧩 Overview
This project uses a **React frontend** and a **Django REST Framework backend**.

---

## ⚙️ Backend Setup (Django)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt # or windowsRequirements.txt on Windows
python manage.py migrate
python manage.py runserver ```