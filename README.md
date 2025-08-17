# FYPBackend – Comprehensive Scheduling System Backend

## Overview

**FYPBackend** is the robust backend powering the advanced academic scheduling platform currently implemented at NED University of Engineering and Technology and used across multiple departments. It exposes a rich set of RESTful APIs for managing users, batches, courses, rooms, preferences, compensatory classes, timetable generations, and more, serving as the data and business logic layer for the [FYPFinal frontend](https://github.com/subhan-uf/fypfinal).

---

## Architecture

- **Framework:** Django + Django REST Framework
- **Database:** PostgreSQL (configurable via environment variables)
- **Auth:** JWT (SimpleJWT), session, and basic authentication support
- **Modular Apps:** Advisors, Users, Scheduler, etc.
- **Admin Interface:** Django admin for direct data management

---

## Major Features & Modules

### User & Role Management

- **DEOs, Advisors, Chairman, Teachers:** CRUD endpoints for all staff roles
- **Authentication:** Secure login/logout for DEOs and Advisors
- **Department & Faculty Management:** Manage academic departments and faculties

### Batch, Section, Course, Room Management

- **Batches/Sections:** Create, update, delete, and query batches and their sections
- **Courses:** Full course lifecycle management, discipline association
- **Rooms:** Manage rooms (labs, lecture halls), capacity, type, and status

### Assignment & Preferences

- **Teacher-Course Assignment:** Assign teachers to courses and batches
- **Batch-Course-Teacher Assignment:** Complex links between batches, courses, and teachers
- **Preferences & Constraints:** Define course time constraints, room preferences, teacher-room assignments

### Timetable Generation & Management

- **Timetable Generation:** Endpoints for generating, retrieving, and managing timetable headers and details (see note below)
- **Compensatory Classes:** Manage compensatory sessions, overlay them on regular timetables
- **Status Tracking:** Published, pending, and historical generations

### Reports & Data Export

- **Timetable Reports:** Downloadable PDF reports of generated timetables for documentation and sharing

### API Explorer & Documentation

- **Browsable API:** Interactive API explorer via DRF, with authentication controls (token, basic, session)
- **Well-documented Endpoints:** Each major entity (user, batch, course, room, preference, generation) exposes comprehensive CRUD operations

---

## Core Business Logic

### Smart Timetable Generation

The heart of the backend is its **extremely comprehensive, custom timetable generation algorithm**. This logic ensures:
- Timetables are generated for batches, teachers, and rooms while respecting a myriad of constraints and preferences.
- Handles edge cases, tight room/time/teacher constraints, compensatory sessions, and dynamic status updates.
- Capable of producing optimal schedules even in highly restrictive scenarios.

> **Note:**  
> The actual timetable generation algorithm is **not public** due to its proprietary and custom nature. This keeps the intellectual property of the solution protected and ensures that the unique scheduling logic remains exclusive to NED University.

---

## Endpoints (Selected Examples)

- `/api/deo/login/`, `/api/deo/logout/` – DEO authentication
- `/api/advisor/login/`, `/api/advisor/logout/` – Advisor authentication
- `/api/advisors/`, `/api/advisors/<id>/` – Advisor management
- `/api/teachers/`, `/api/teachers/<id>/` – Teacher management
- `/api/rooms/`, `/api/rooms/<id>/` – Room management
- `/api/courses/`, `/api/courses/<id>/` – Course management
- `/api/batches/`, `/api/batches/<id>/` – Batch management
- `/api/sections/`, `/api/sections/<id>/` – Section management
- `/api/teacher-course-assignments/`, `/api/teacher-course-assignments/<id>/` – Teacher-course assignments
- `/api/batch-course-teacher-assignments/`, `/api/batch-course-teacher-assignments/<id>/` – Batch-course-teacher assignments
- `/api/timetable-header/`, `/api/timetable-header/<id>/` – Timetable meta-information
- `/api/timetable-detail/`, `/api/timetable-detail/<id>/` – Timetable slots & details
- `/api/compensatory/`, `/api/compensatory/<id>/` – Compensatory class management
- `/api/course-preference-constraints/`, `/api/course-preference-constraints/<id>/` – Time constraints for courses
- `/api/teacher-room-preference/`, `/api/teacher-room-preference/<id>/` – Preferences for teacher-room assignments
- `/api/discipline/`, `/api/discipline/<id>/` – Discipline management

> See the API documentation or DRF browsable API for the full list and details.

---

## Integration with Frontend

- Designed to work seamlessly with [FYPFinal](https://github.com/subhan-uf/fypfinal)
- All business logic, data validation, and scheduling computation are handled here; frontend is a visualization and interaction layer

---

## Entity Relationship Diagram (ERD)

![Demo](https://i.imgur.com/OKUrdz4.png)


---

## Deployment & Adoption

**This Resource Scheduling System is currently implemented at NED University of Engineering and Technology and being used by multiple departments.**  
It supports faculty, advisors, and administrative staff to automate and optimize scheduling workflows across the university.

---
Click the image below to see a working demo:

[![Watch Demo](https://img.youtube.com/vi/2wzoR2I6JvY/hqdefault.jpg)](https://youtu.be/2wzoR2I6JvY)


## License

Distributed under the MIT License.

---

## Support

For issues, feature requests, or questions, [open an issue](https://github.com/subhan-uf/fypbackend/issues) or contact the repository owner.

---
