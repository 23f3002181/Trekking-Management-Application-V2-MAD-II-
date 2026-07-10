# Trekking Management Application (TMA) - V2

## Overview
The Trekking Management Application is a decoupled, full-stack web platform designed to streamline the management and booking of trekking activities. It provides a structured, role-based system with tailored dashboards for Administrators, Trek Staff, and Trekkers (Users). 

The backend is powered by Python and Flask, handling RESTful API routing, Role-Based Access Control (RBAC), and asynchronous background jobs via Celery and Redis. The frontend is a Single Page Application (SPA) built with Vue.js 3 and Vite, offering a dynamic and reactive user interface.

## Key Features

### Role-Based Access Control (RBAC)
*   **Admin Dashboard:** Complete system oversight. Create and manage trekking routes, assign staff to treks, oversee system-wide booking statistics, and manage users (including whitelisting/blacklisting).
*   **Staff Dashboard:** Dedicated interface for trek guides. View assigned treks, manage available slots, update trek statuses (e.g., Open, Started, Completed), and view participant lists.
*   **User (Trekker) Dashboard:** Search, filter, and book available treks. Manage personal profile, view booking history, and cancel active bookings.

### Core Technical Features
*   **Decoupled Architecture:** Clean separation of concerns between the Vue.js frontend and Flask backend.
*   **Asynchronous Processing:** Celery integrated with Redis to handle background tasks, such as generating and downloading user booking history CSVs without blocking the main UI thread.
*   **Data Caching:** Redis caching implemented for frequently accessed API endpoints (like public analytics and open treks) to optimize performance.
*   **State Management:** Frontend state (like authentication and trek data) is managed efficiently using Vue stores (e.g., `trekStore.js`).
*   **Analytics Visualization:** Public analytics dashboard showing popular treks, booking trends, and trek statuses.

## 🛠️ Technology Stack

### Backend
*   **Framework:** Python 3, Flask, Flask-Security
*   **Database:** SQLite, SQLAlchemy (ORM)
*   **Caching & Queue:** Redis
*   **Background Jobs:** Celery (Workers & Beat Schedule)

### Frontend
*   **Framework:** Vue.js 3
*   **Build Tool:** Vite
*   **Routing & State:** Vue Router, Pinia/Vuex
*   **Styling:** Bootstrap 5, Custom CSS

## 📂 Project Structure

```text
TREKKING_MANAGEMENT_APPLICATION/
│
├── backend/                  # Flask Backend Directory
│   ├── app.py                # Main Flask application entry point
│   ├── cache.py              # Redis caching configuration
│   ├── tasks.py              # Celery asynchronous task definitions
│   ├── requirements.txt      # Python dependencies
│   ├── models/               # SQLAlchemy Database Models
│   │   ├── trek_models.py
│   │   └── user_models.py
│   └── routes/               # Modularized Blueprint Routes
│       ├── admin_routes.py
│       ├── auth_routes.py
│       ├── staff_routes.py
│       └── user_routes.py
│
└── frontend/                 # Vue.js Frontend Directory
    ├── package.json          # Node dependencies and scripts
    ├── vite.config.js        # Vite configuration
    ├── index.html            # Entry HTML file
    └── src/
        ├── App.vue           # Root Vue component
        ├── main.js           # Vue application instance
        ├── router/           # Vue Router configuration
        ├── stores/           # Global state management
        └── components/       # Reusable Vue components
            ├── admin/        # Admin dashboard components
            ├── staff/        # Staff dashboard components
            └── user/         # Trekker dashboard components

