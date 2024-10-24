Oyla - Free Online Educational Platform
Oyla is a free, user-friendly online platform designed to deliver a wide range of educational courses. The platform caters to students, instructors, and administrators, providing tools for course enrollment, progress tracking, content management, assessments, and platform management.

Table of Contents
Features
Roles and Permissions
API Endpoints
Functional Requirements
Non-Functional Requirements
Installation
Usage
Contributing
License
Features
For Students
Browse and enroll in courses for free.
Track learning progress through a personal dashboard.
Watch course videos and complete quizzes at the end of each module.
Receive instant feedback on test results, including correct answers.
Engage with artificial intelligence to ask questions related to course topics.
Participate in course-specific discussion forums to interact with instructors and other students.
For Instructors
Create, edit, and delete course content, including video lessons and quizzes.
Track the progress and performance of students enrolled in courses.
For Administrators
Manage user accounts, roles, and permissions.
Approve new courses and monitor platform operations.
Customize platform settings, including themes and categories.
Oversee platform activity and content quality.
Roles and Permissions
Students:

Enroll in courses and track progress.
Take tests and receive feedback.
Ask AI-based questions related to course topics.
Instructors:

Create, manage, and update course content.
Design tests to assess students' understanding.
Monitor student progress and performance.
Administrators:

Manage user roles, permissions, and platform operations.
Approve new course content.
Customize platform settings.
API Endpoints
User Authentication
Register User: POST /register/
Login User: POST /login/
Course Management
Get Course List: GET /course/api/courses/
Get Topics List: GET /course/api/courses/<int:course_id>/topics/
Get Videos: GET /course/api/courses/<int:course_id>/topics/<int:topic_id>/videos
Test Management
Get All Tests: GET /quiz/api/questions/
Get Tests for Video: GET /quiz/api/test/<int:video_id>/
Submit Test: POST /quiz/api/submit_test/<int:video_id>/
Video Management
Get Streaming Video: GET /video/api/stream/<int:pk>/
Get Video: GET /video/api/video/<int:pk>/
Get List Video: GET /video/api/videos/<int:topic_id>/
Functional Requirements
User Authentication: Secure registration and login using email and password.
Course Management: Browse and enroll in free courses. Instructors can create and manage course content, including videos and quizzes.
Learning Management: Courses consist of multiple modules. Students track progress and complete quizzes to assess understanding.
Assessment and Feedback: Immediate feedback for quizzes with correct answers and scores.
Administrative Features: Administrators manage users, platform settings, and content approval.
Non-Functional Requirements
Performance: The platform should handle at least 1000 concurrent users with pages loading within 3 seconds.
Scalability: Supports scaling to accommodate more users and courses.
Usability: Intuitive interface with key actions completed in 3 clicks.
Security: Secure data storage with encryption and protection against vulnerabilities.
Compatibility: Works on major browsers and mobile devices with responsive design.
Maintainability: Modular and well-documented code, with version control using GitHub.
Availability: 99.5% or higher uptime.
Backup and Recovery: Regular database backups and disaster recovery plans.
Installation
Prerequisites
Python 3.x
Django 4.x
Docker (optional)
PostgreSQL (or any other preferred database)
Steps
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/oyla-platform.git
cd oyla-platform
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the database:

bash
Copy code
python manage.py migrate
Run the server:

bash
Copy code
python manage.py runserver
Access the platform at http://127.0.0.1:8000/.

Usage
Students: Register, browse courses, and track progress.
Instructors: Log in and create or manage your courses.
Administrators: Manage platform users, content, and operations through the admin panel.
Contributing
We welcome contributions! Please follow the steps below:

Fork the repository.
Create a new branch for your feature or bug fix.
Submit a pull request with a clear description of the changes.
License
This project is licensed under the MIT License. See the LICENSE file for details.
