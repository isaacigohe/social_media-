# SocialMedia Django API

A full-featured social media REST API built with Django & DRF.

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations
python manage.py migrate

# 4. Create superuser (optional)
python manage.py createsuperuser

# 5. Run server
python manage.py runserver
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Create new account |
| POST | `/api/auth/login/` | Login (get JWT tokens) |
| POST | `/api/auth/token/refresh/` | Refresh JWT access token |
| GET  | `/api/auth/me/` | Get current user profile |

### Profiles
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/profiles/{user_id}/` | Get user profile |
| PUT/PATCH | `/api/profiles/{user_id}/` | Update own profile |

### Posts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/posts/` | News feed (followed users) |
| POST | `/api/posts/` | Create new post |
| GET | `/api/posts/{post_id}/` | Get post details |
| PUT/PATCH | `/api/posts/{post_id}/` | Edit own post |
| DELETE | `/api/posts/{post_id}/` | Delete own post |

### Comments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/posts/{post_id}/comments/` | List post comments |
| POST | `/api/posts/{post_id}/comments/` | Add comment |
| PUT/PATCH | `/api/comments/{comment_id}/` | Edit own comment |
| DELETE | `/api/comments/{comment_id}/` | Delete own comment |

### Likes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/posts/{post_id}/like/` | Like a post |
| DELETE | `/api/posts/{post_id}/like/` | Unlike a post |
| POST | `/api/comments/{comment_id}/like/` | Like a comment |
| DELETE | `/api/comments/{comment_id}/like/` | Unlike a comment |

### Follow
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/{user_id}/follow/` | Follow a user |
| DELETE | `/api/users/{user_id}/follow/` | Unfollow a user |

### Search & Discovery
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/search/users/?query={q}` | Search users |
| GET | `/api/notifications/` | Get notifications |

## Authentication

All protected endpoints require a Bearer token:
```
Authorization: Bearer <access_token>
```

## Creating a Post with Hashtags

```json
POST /api/posts/
{
  "content": "Hello world! #django #python",
  "hashtag_names": ["django", "python"]
}
```
