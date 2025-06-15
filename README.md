# 📝 WXP Blog

A dynamic blog website where users can explore blog posts, read full articles, and interact with clean UI components. Built using **Django** and styled with **Tailwind CSS**, this project reflects a fully functional blogging platform ideal for sharing content and practicing full-stack development.

🔗 **Live Demo**: [https://wxp-blog.onrender.com](https://wxp-blog.onrender.com)

---

## 🚀 Features

- 📰 Display all blog posts with pagination  
- 🔍 View detailed blog content by clicking "Read More"  
- 🖼️ Post images supported with responsive layout  
- 👤 Admin panel to create, update, or delete posts  
- 🌙 Clean, modern UI using Tailwind CSS  
- 📱 Fully responsive design for mobile & desktop  

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)  
- **Frontend**: Bootstrap5, CSS3, HTML5 
- **Database**: SQLite (switchable to PostgreSQL or MySQL)  
- **Deployment**: Render  

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/wxp-blog.git
cd wxp-blog
```

### 2. Create and activate a virtual environment

```bash
python -m venv env
```

- **Windows:**
  ```bash
  env\Scripts\activate
  ```
- **Linux/Mac:**
  ```bash
  source env/bin/activate
  ```

### 3. Install project dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

Now open `http://127.0.0.1:8000/` in your browser to view the project.

### 6. (Optional) Create a superuser

```bash
python manage.py createsuperuser
```

---

## 👤 Author

- **Md. Waliullah**  
  GitHub: [@waliullah9277](https://github.com/waliullah9277)  
  Email: waliullah9252@gmail.com  

---

## 📄 License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and improve as needed.
