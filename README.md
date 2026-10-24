# CodeAlpha_SocialMediaPlatform

A social media web application built using Django that allows users to connect, share posts, and interact with other users. The platform supports text, image, and video posts, along with likes, comments, and a personalized feed.

## Features

- **User Authentication:** User registration, login, and logout.
- **User Profiles:** View and edit profile information, including bio and profile picture.
- **Create Posts:** Share text updates, images, and videos.
- **Personalized Feed:** View your posts and posts from users you follow.
- **Like and Unlike Posts:** Interact with posts shared by other users.
- **Comments:** Add comments to posts.
- **Follow and Unfollow:** Follow users to see their content in your feed.
- **Discover Users:** Explore other users on the platform.
- **Post Management:** Users can delete their own posts.
- **Responsive Interface:** Clean and user-friendly design.

## Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript, Bootstrap (if used in your project)
- **Database:** SQLite by default, unless configured otherwise
- **Media Handling:** Django ImageField and FileField

## Project Structure

```text
CodeAlpha_SocialMediaPlatform/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── social/
│   ├── migrations/
│   ├── templates/
│   │   └── social/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
└── your_project_folder/
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

*Note: Your actual Django project folder name and file structure may differ.*

## Prerequisites

Install the following before running the project:

- Python 3.11 or another Python version compatible with your installed Django version
- pip
- Git (optional, for cloning the repository)

## Installation and Setup

### 1. Clone the Repository

Replace `YOUR_USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR_USERNAME/CodeAlpha_SocialMediaPlatform.git
cd CodeAlpha_SocialMediaPlatform
```

Alternatively, download the repository as a ZIP file and extract it.

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

The migration files already included in the repository should be applied by `migrate`. Usually, you do not need to generate new migrations unless you have changed the models.

### 5. Create an Administrator Account (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an administrator account.

### 6. Run the Development Server

```bash
python manage.py runserver
```

## Media Files

The application supports profile pictures and image/video uploads.

Uploaded media files are stored locally according to the Django media settings. User-uploaded media files are not included in this repository.

To display uploaded media correctly during local development, ensure that your Django project has the appropriate `MEDIA_URL` and `MEDIA_ROOT` settings and that media URLs are configured in the main URL configuration when `DEBUG` is enabled.

## Database

The application uses Django's configured database. If SQLite is configured, Django creates a local `db.sqlite3` database when migrations are applied.

A fresh installation starts with a new database, so users and posts from the original development environment will not automatically appear.

## Future Enhancements

Potential future improvements include:

- Notifications for likes, comments, and followers
- Direct messaging between users
- Post bookmarking and sharing
- Hashtags and Explore page
- Stories and short-video features
- Enhanced privacy settings

