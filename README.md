# CampusEvents - College Event Management Web Application

A full-stack, responsive web application engineered for college students and academic administrators to create, discover, register, and manage campus events, hackathons, sports championships, workshops, and cultural fests.

---

## Architecture Overview

```
campusevents/
├── backend/                  # Flask REST API (Python 3.13)
│   ├── authentication/       # JWT Handler, Password Hashing, Role Decorators
│   ├── models/               # Validation schemas for events, students, registrations
│   ├── routes/               # Modular REST endpoints (auth, events, registrations, notifs, analytics)
│   ├── services/             # Auto database seeder with 7 categories of realistic campus events
│   ├── database.py           # Hybrid PyMongo Engine with auto zero-config local JSON persistence
│   ├── app.py                # Main Flask entrypoint with CORS
│   └── test_api.py           # Backend automated test suite (100% pass)
└── frontend/                 # React 19 + TypeScript + Vite + Tailwind CSS v4
    ├── src/
    │   ├── components/       # Layout, EventCard, TicketModal, RegisterModal, Admin modals
    │   ├── pages/            # Landing, Login, Register, Dashboards, Events, Calendar, Pass Roster
    │   ├── services/         # Centralized API service with Bearer auth interceptor
    │   ├── hooks/            # useAuth context provider
    │   └── types/            # Strict TypeScript interfaces
    └── dist/                 # Production optimized bundle
```

---

## Pre-Configured Demo Accounts

For fast review and demonstration, one-click demo login buttons are provided directly on the Login page:

| Role | Email | Password | Features |
|---|---|---|---|
| **Student** | `student@campus.edu` | `password123` | Event registration, digital E-Pass with QR code, My Passes, interactive calendar |
| **Administrator** | `admin@campus.edu` | `admin123` | Analytics dashboard, Event creation & editing, Student attendee roster with CSV export, Campus Broadcast alerts |

---

## 7 Standard Event Categories
- **Hackathons** (e.g. *HackSphere 2026: 36-Hour National Hackathon*)
- **Technical** (e.g. *RoboWars: Combat Robotics & Autonomous Drones*)
- **Cultural** (e.g. *Tarang 2026: Annual Inter-College Cultural Fest*)
- **Sports** (e.g. *Annual Inter-Department Athletics & Sports Meet*)
- **Workshops** (e.g. *Cloud Native & DevOps Hands-on Workshop*)
- **Seminars** (e.g. *Symposium on Generative AI & Quantum Computing*)
- **Competitions** (e.g. *CodeSprint: Speed Algorithm Challenge*)

---

## How to Run

### Quick One-Click (Windows)
Double-click `run_campusevents.bat` in the root folder.

### Manual Launch

**1. Backend**:
```bash
cd backend
.\venv\Scripts\python app.py
```
*Backend runs on `http://127.0.0.1:5000`*

**2. Frontend**:
```bash
cd frontend
npm run dev
```
*Frontend runs on `http://localhost:5173`*

**3. Run Automated Tests**:
```bash
cd backend
.\venv\Scripts\python test_api.py
```
