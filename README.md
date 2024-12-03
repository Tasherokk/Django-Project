# Oyla - Free Online Educational Platform

**Oyla** is a free, user-friendly online platform designed to deliver a wide range of educational courses. The platform caters to students, instructors, and administrators, providing tools for course enrollment, progress tracking, content management, assessments, and platform management.

## Table of Contents
- [Features](#features)
- [Roles and Permissions](#roles-and-permissions)
- [API Endpoints](#api-endpoints)
- [Functional Requirements](#functional-requirements)
- [Non-Functional Requirements](#non-functional-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

### For Students
- Browse and enroll in courses for free.
- Track learning progress through a personal dashboard.
- Watch course videos and complete quizzes at the end of each module.
- Receive instant feedback on test results, including correct answers.
- Engage with artificial intelligence to ask questions related to course topics.
- Participate in course-specific discussion forums to interact with instructors and other students.

### For Instructors
- Create, edit, and delete course content, including video lessons and quizzes.
- Track the progress and performance of students enrolled in courses.

### For Administrators
- Manage user accounts, roles, and permissions.
- Approve new courses and monitor platform operations.
- Customize platform settings, including themes and categories.
- Oversee platform activity and content quality.

## Roles and Permissions

1. **Students**:
   - Enroll in courses and track progress.
   - Take tests and receive feedback.
   - Ask AI-based questions related to course topics.

2. **Instructors**:
   - Create, manage, and update course content.
   - Design tests to assess students' understanding.
   - Monitor student progress and performance.

3. **Administrators**:
   - Manage user roles, permissions, and platform operations.
   - Approve new course content.
   - Customize platform settings.

## API Endpoints

### User Authentication
- **Register User**: `POST /register/`
- **Login User**: `POST /login/`

### Course Management
- **Get Course List**: `GET /course/api/courses/`
- **Get Topics List**: `GET /course/api/courses/<int:course_id>/topics/`
- **Get Videos**: `GET /course/api/courses/<int:course_id>/topics/<int:topic_id>/videos`

### Test Management
- **Get All Tests**: `GET /quiz/api/questions/`
- **Get Tests for Video**: `GET /quiz/api/test/<int:video_id>/`
- **Submit Test**: `POST /quiz/api/submit_test/<int:video_id>/`

### Video Management
- **Get Streaming Video**: `GET /video/api/stream/<int:pk>/`
- **Get Video**: `GET /video/api/video/<int:pk>/`
- **Get List Video**: `GET /video/api/videos/<int:topic_id>/`

## Functional Requirements
1. **User Authentication**: Secure registration and login using email and password.
2. **Course Management**: Browse and enroll in free courses. Instructors can create and manage course content, including videos and quizzes.
3. **Learning Management**: Courses consist of multiple modules. Students track progress and complete quizzes to assess understanding.
4. **Assessment and Feedback**: Immediate feedback for quizzes with correct answers and scores.
5. **Administrative Features**: Administrators manage users, platform settings, and content approval.

## Non-Functional Requirements
1. **Performance**: The platform should handle at least 1000 concurrent users with pages loading within 3 seconds.
2. **Scalability**: Supports scaling to accommodate more users and courses.
3. **Usability**: Intuitive interface with key actions completed in 3 clicks.
4. **Security**: Secure data storage with encryption and protection against vulnerabilities.
5. **Compatibility**: Works on major browsers and mobile devices with responsive design.
6. **Maintainability**: Modular and well-documented code, with version control using GitHub.
7. **Availability**: 99.5% or higher uptime.
8. **Backup and Recovery**: Regular database backups and disaster recovery plans.

## Installation

### Prerequisites
- Python 3.x
- Django 4.x
- Docker (optional)
- PostgreSQL (or any other preferred database)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/oyla-platform.git
   cd oyla-platform
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```bash
   python manage.py migrate  
   ```
4. Run the server:
   ```bash
   python manage.py runserver
   ```
