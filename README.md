# SociaSphere

Social networking platform that enables users to create profiles, share content, discover communities, and engage through an interactive social feed.

**Live:** https://sociasphere.onrender.com/

**Demo:** https://youtu.be/pIHj1mT5XzU

## Problem

Online communities rely on user-generated content, social connections, and content discovery. Building these experiences requires authentication systems, profile management, relationship modeling, feed generation, and engagement workflows.

SociaSphere explores these core social platform concepts through a community-focused web application.

## Features

### User Authentication

* User registration
* Secure login and logout
* Session-based authentication
* User account management

### Profile Management

Users can:

* Update usernames
* Upload profile images
* Add personal bios
* Attach social media links
* View personal activity

### Content Sharing

* Create posts
* Publish ideas
* Share content with the community
* Manage personal posts

### Social Interactions

* Follow users
* View follower counts
* View following counts
* Like posts
* Share posts

### Discovery

#### User Search

* Search platform users
* Discover creators
* Follow accounts directly

#### Post Search

* Search content across the platform
* Discover community discussions

#### Profile Directory

* Browse community members
* Access user profiles
* Explore new accounts

## Architecture

SociaSphere follows a server-side rendered architecture using Django.

### Core Modules

* Authentication System
* Profile Management
* Feed Generation
* User Discovery
* Post Management
* Social Relationship System

### Data Relationships

The platform models:

* Users
* Profiles
* Posts
* Followers
* Following relationships
* Likes

These relationships drive feed generation and social interactions throughout the application.

## Tech Stack

### Backend

* Python
* Django

### Database

* PostgreSQL

### Frontend

* HTML
* CSS
* Django Templates

### Media Management

* Pillow

## Key Engineering Highlights

* Built secure session-based authentication workflows using Django's authentication framework.
* Developed relationship-driven social features including follows, likes, and profile interactions.
* Implemented user and content discovery through search functionality.
* Optimized feed retrieval using relationship prefetching and database query improvements.
* Designed user profile management workflows with media upload support.

## Project Structure

```text
SociaSphere/
├── users/
├── profiles/
├── posts/
├── templates/
├── static/
├── media/
├── manage.py
└── README.md
```

## Local Development

### Clone Repository

```bash
git clone https://github.com/kvdhanush06/SociaSphere.git

cd SociaSphere
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py migrate
```

### Start Development Server

```bash
python manage.py runserver
```
