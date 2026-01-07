# 🚀 OSS Contribution Tracker

A Django-based web application that helps you track, analyze, and visualize your open-source contributions using GitHub data — including repositories, pull requests, and issues.

Perfect for developers who want insights into their OSS journey 📊

---

## ✨ Features

* 🔐 GitHub OAuth authentication
* 📦 Fetch GitHub repositories, pull requests & issues
* 📊 Contribution dashboard with monthly analytics
* 📈 Interactive charts for PRs and issues
* 🧱 Clean, service-based backend architecture
* 🌱 Beginner-friendly and open-source ready

---

## 🛠️ Tech Stack

* **Backend:** Django, Python
* **Auth:** GitHub OAuth
* **APIs:** GitHub REST API
* **Database:** SQLite (default, easily configurable)
* **Frontend:** Django Templates + Charts

---

## 🚀 Getting Started (Run Locally)

Follow these steps to set up the project on your local machine.

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2️⃣ Create & activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
# venv\Scripts\activate    # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Apply database migrations

```bash
python manage.py migrate
```

### 5️⃣ Run the development server

```bash
python manage.py runserver
```

### 6️⃣ Open in your browser 🌐

```
http://127.0.0.1:8000/
```

### 7️⃣ Login with GitHub 🔑

* Click **Login with GitHub**
* Authorize the application
* Start tracking your contributions 🎉

---

## 📌 What This Project Does

* Connects securely with GitHub using OAuth
* Fetches and stores contribution data
* Displays contribution insights in a clean dashboard
* Helps developers understand their open-source activity

---

## 🎯 Why This Project?

This project was built to:

* Learn real-world Django backend patterns
* Understand GitHub API integrations
* Practice analytics & dashboard development
* Build an open-source friendly codebase
* Help developers track their OSS growth 📈

---

## 👥 Who Can Contribute?

* 🎓 Students learning Django / Backend / Frontend
* 🌱 Developers new to open source
* 📊 Anyone interested in GitHub analytics
* 🧠 Curious builders who love dashboards

**Beginner-friendly contributions are highly welcome!**

---

## 🚧 Project Status

🛠️ **Actively evolving**

More features, optimizations, and UI improvements are planned. Stay tuned and feel free to suggest ideas!

---

## 🤝 Contributions

Contributions, ideas, and improvements are welcome 💡

Feel free to:

* Open an Issue
* Submit a Pull Request
* Suggest new features or improvements

---

## ❤️ Acknowledgements

Built with ❤️ using **Django & Python**

Inspired by the open-source community 🌍