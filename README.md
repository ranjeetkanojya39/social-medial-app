# Social Media App 🌐

A feature-rich Django-based social media application that allows users to connect, share posts, and engage with their community. The app is deployed on Render and uses Cloudinary for image storage.

**Live Demo:** https://social-medial-app.onrender.com

---

## 📸 Screenshots

<!--
Yahan apne app ke actual screenshots daalo. Steps:
1. Repo mein ek "screenshots/" folder banao (root level pe, README.md ke saath)
2. Feed, Profile, Explore, Login page ke screenshots us folder mein daalo (e.g. feed.png, profile.png)
3. Neeche wali syntax use karke embed karo:
-->

| Feed | Profile | Explore |
|------|---------|---------|
| ![Feed](screenshots/feed.png) | ![Profile](screenshots/profile.png) | ![Explore](screenshots/explore.png) |

---

## ✨ Features

### 👤 User Authentication
- **Sign Up:** Register with username, email, and password
- **Login/Logout:** Secure authentication system
- **Profile Management:** Create and customize user profiles with bio, location, and profile picture

### 📸 Posts & Content
- **Create Posts:** Upload images with captions
- **Delete Posts:** Remove your own posts
- **View Feed:** See posts from users you follow
- **Explore:** Browse all posts from the community

### ❤️ Engagement
- **Like/Unlike Posts:** Toggle likes on any post
- **Like Counter:** Track the number of likes per post

### 👥 Social Features
- **Follow/Unfollow:** Build your network by following other users
- **User Profiles:** View follower/following counts and user statistics
- **Search:** Find users and posts by username or caption

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend language (95.8%) |
| Django | Web framework |
| SQLite3 | Database |
| Cloudinary | Image storage and CDN |
| HTML/CSS/JavaScript | Frontend (1.7% + 1.7%) |
| Gunicorn | WSGI server |
| WhiteNoise | Static file serving |
| Pillow | Image processing |

### Key Dependencies
```
Django==6.0.4
django-cloudinary-storage==0.3.0
cloudinary==1.44.2
pillow==12.2.0
gunicorn==26.0.0
whitenoise==6.12.0
python-dotenv==1.2.2
```

---

## 📁 Project Structure

```
social-medial-app/
├── socialmedia/              # Main Django project settings
│   ├── settings.py           # Django configuration
│   ├── urls.py               # URL routing
│   ├── wsgi.py                # WSGI application
│   └── asgi.py                # ASGI application
├── userauth/                 # User authentication app
│   ├── models.py             # Database models
│   ├── views.py               # View logic
│   ├── urls.py                # App URLs
│   └── admin.py               # Django admin configuration
├── templates/                 # HTML templates
│   ├── main.html               # Feed page
│   ├── profile.html            # User profile
│   ├── signup.html             # Sign up page
│   ├── loginn.html              # Login page
│   ├── explore.html            # Explore all posts
│   └── search_user.html         # Search results
├── static/                    # CSS, JavaScript, images
├── screenshots/                # README screenshots
├── media/                      # Local media uploads (development)
├── manage.py                   # Django management script
├── requirements.txt             # Python dependencies
├── db.sqlite3                    # SQLite database
└── README.md                     # This file
```

---

## 📊 Database Models

**Profile**
- User profile information
- Bio, location, and profile image
- Links to Django User model

**Post**
- User-generated posts with images
- Caption and timestamp
- Like counter
- Ordered by creation date (newest first)

**LikePost**
- Tracks which users liked which posts
- Prevents duplicate likes with unique constraint

**Followers**
- Manages follow relationships between users
- Prevents users from following themselves
- Prevents duplicate follow relationships

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Virtual environment

### 1. Clone the Repository
```bash
git clone https://github.com/ranjeetkanojya39/social-medial-app.git
cd social-medial-app
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Cloudinary Configuration (for production)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 5. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```
Visit http://localhost:8000 in your browser.

---

## 🌐 Deployment on Render

### Prerequisites
- Render account (https://render.com)
- Cloudinary account (https://cloudinary.com)
- GitHub repository with this code

### Steps
1. **Create Web Service on Render**
   - Connect your GitHub repository
   - Select Python as runtime
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn socialmedia.wsgi`

2. **Set Environment Variables in Render Dashboard**
   - `SECRET_KEY`: Generate a secure key
   - `DEBUG`: False
   - `CLOUDINARY_CLOUD_NAME`: Your Cloudinary cloud name
   - `CLOUDINARY_API_KEY`: Your Cloudinary API key
   - `CLOUDINARY_API_SECRET`: Your Cloudinary API secret

3. **Deploy**
   - Click Deploy
   - Monitor the build logs

---

## 📝 API Endpoints

### Authentication
| Endpoint | Method | Description |
|---|---|---|
| `/signup/` | POST | Register a new user |
| `/loginn/` | POST | Login user |
| `/logoutt/` | GET | Logout user |

### Posts
| Endpoint | Method | Description |
|---|---|---|
| `/upload/` | POST | Create a new post |
| `/delete/<id>/` | GET | Delete a post |

### Feed & Explore
| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | View personalized feed |
| `/explore/` | GET | View all posts |

### Profiles
| Endpoint | Method | Description |
|---|---|---|
| `/profile/<username>/` | GET/POST | View/edit user profile |

### Social
| Endpoint | Method | Description |
|---|---|---|
| `/like/<id>/` | GET | Like/unlike a post |
| `/follow/` | POST | Follow/unfollow a user |
| `/search/` | GET | Search users and posts |

---

## 🔐 Security Features
- **Django CSRF Protection:** All forms include CSRF tokens
- **Password Validation:** Django's built-in password validators
- **SQLite with Django ORM:** Prevents SQL injection
- **Unique Constraints:** Database-level prevention of duplicate follows/likes
- **WhiteNoise:** Secure static file serving
- **Environment Variables:** Sensitive data kept in `.env`

---

## 🤝 Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 📄 License
This project is open source and available under the MIT License.

---

## 👨‍💻 Author
**Ranjeet Kanojya**
- GitHub: [@ranjeetkanojya39](https://github.com/ranjeetkanojya39)
- Email: ranjeetkanojya39@gmail.com

---

## 🙏 Acknowledgments
- Django framework documentation
- Cloudinary for image storage
- Render for hosting
- Font Awesome for icons

---

## ⚠️ Known Issues & Future Improvements

### To-Do
- [ ] Implement post comments
- [ ] Add direct messaging feature
- [ ] Add notification system
- [ ] User profile verification
- [ ] Better error handling and logging
- [ ] Add hashtags support
- [ ] Implement infinite scroll on feed
- [ ] Add user recommendations

### Known Limitations
- Single image per post
- No edit post functionality
- No post scheduling
- Limited search functionality
- Comments not yet implemented

---

## 📞 Support
For issues, bugs, or feature requests, please open an issue on GitHub Issues.

**Last Updated:** July 2026
