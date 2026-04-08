# 🧠 Note Sharing Platform (Django)

A simple Django app to create, manage, and share notes with Markdown support.

---

## 🚀 Features

* Create, edit, delete notes
* Public/private sharing
* Unique shareable links (UUID)
* Markdown formatting
* Version history

---

## ⚙️ Setup

```bash
git clone https://github.com/your-username/notes-project.git
cd notes-project

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install django markdown

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 🌐 Usage

* Login to create notes
* Set notes to **public** to share via link
* Access shared notes at:

  ```
  /share/<uuid>/
  ```

---

## 🛠️ Tech Stack

* Python, Django
* SQLite
* Markdown

---

## 📄 License

MIT
