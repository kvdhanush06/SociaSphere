# SociaSphere — Social Networking & Feed Platform

**SociaSphere** is a Django-based social networking platform for profiles, user-generated posts, communities, content discovery, social relationships, and interactive feeds.

**Live:** https://sociasphere.onrender.com/

**Demo:** https://youtu.be/pIHj1mT5XzU

**Repository:** https://github.com/kvdhanush06/SociaSphere

## Problem

Building a social application requires secure authentication, profile management, relationship modeling, feed generation, content discovery, and engagement workflows. SociaSphere explores these core social-platform engineering concepts through a community-focused web application.

## Features

### User Authentication

- User registration
- Secure login and logout
- Session-based authentication
- User account management

### Profile Management

- Username updates
- Profile images
- Personal bios
- Social links
- Personal activity

### Content Sharing

- Create and manage posts
- Publish ideas and community content

### Social Interactions

- Follow users
- Follower and following counts
- Like posts
- Share posts

### Discovery

- Search users and creators
- Search posts and discussions
- Browse community profiles

## Architecture

SociaSphere follows a server-side rendered architecture using Django.

### Core Modules

- Authentication System
- Profile Management
- Feed Generation
- User Discovery
- Post Management
- Social Relationship System

### Data Relationships

The application models users, profiles, posts, followers, following relationships, and likes. These relationships drive feed generation and social interactions.

## Tech Stack

- Python
- Django
- SQLite
- HTML/CSS
- Django Templates
- Pillow

## Key Engineering Highlights

- Built secure session-based authentication workflows using Django's authentication framework.
- Developed relationship-driven social features including follows, likes, and profile interactions.
- Implemented user and content discovery through search functionality.
- Optimized feed retrieval using relationship prefetching and database query improvements.
- Designed profile management workflows with media upload support.

## Project Structure

```text
SociaSphere/
├── sociasphere/
│   ├── dashboard/
│   ├── sociasphere/
│   ├── templates/
│   └── static/
├── manage.py
└── README.md
```

## Local Development

```bash
git clone https://github.com/kvdhanush06/SociaSphere.git
cd SociaSphere
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Product & Creator

SociaSphere is a software product published by **Venkata Dhanush Kakarlamudi** under the AllKVD project portfolio.

- **Product:** https://sociasphere.onrender.com/
- **Creator:** https://allkvd.dev/
- **Portfolio:** https://portfolio.allkvd.dev/
- **GitHub:** https://github.com/kvdhanush06
- **Resume:** https://drive.google.com/file/d/1NCT6ZCa_HfxCdScqI-1Q2yA6y2c7O-qA/view
