# DeepScan – Deepfake Detection Platform

A full-stack web application for detecting deepfakes in videos using deep learning. Built with a modular FastAPI backend, TensorFlow-based detection, LIME explainability, and Supabase for cloud storage and PostgreSQL persistence.

## Features

- **Deepfake Detection** – TensorFlow model analyzes uploaded videos frame-by-frame
- **LIME Explainability** – Visual explanations highlighting regions that influenced the model's prediction
- **JWT Authentication** – Secure stateless auth with role-based access control
- **Argon2 Password Hashing** – Industry-standard password security via Passlib
- **Smart Storage** – Anonymous users get local temp storage; authenticated users get persistent Supabase cloud storage
- **Scan History** – Authenticated users can view and track all previous scans
- **Analytics Dashboard** – SQL aggregations for scan statistics
- **Modular Router Architecture** – Separate FastAPI routers for auth, detection, scans, and analytics

## Tech Stack

- **Framework:** FastAPI
- **Language:** Python
- **ML / CV:** TensorFlow, OpenCV, scikit-image, LIME, NumPy, Matplotlib
- **Database:** PostgreSQL via Supabase (SQLAlchemy ORM)
- **Cloud Storage:** Supabase Storage
- **Auth:** JWT (python-jose), Argon2 / bcrypt (Passlib)
- **Frontend:** HTML, CSS, JavaScript (served via FastAPI static files)

## Project Structure

```
deepscan/
├── api/
│   ├── auth.py             # Register, login, JWT token handling
│   ├── detect.py           # Video upload and deepfake detection endpoint
│   └── scans.py            # Scan history and analytics
├── database/
│   ├── base.py             # SQLAlchemy engine and session setup
│   └── supabase_client.py  # Supabase client initialization
├── templates/              # HTML pages (index, login, signup, dashboard, history)
├── static/                 # CSS, JS assets
├── temp_lime/              # Temporary LIME explainability output files
├── main.py                 # FastAPI app entry point
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL database (local or Supabase)
- Supabase project (for cloud storage)

### Installation

```bash
git clone https://github.com/ymanocha/deepscan.git
cd deepscan
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql+psycopg2://your_db_connection_string
SECRET_KEY=your_jwt_secret_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_service_role_key
```

### Run the Server

```bash
uvicorn main:app --reload
```

Server runs on `http://localhost:8000` by default.

## API Endpoints

### Auth

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register a new user | No |
| POST | `/api/auth/login` | Login and receive JWT | No |

### Detection

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/scans/detect` | Upload video for deepfake detection | Optional |

### Scans

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/scans/history` | Get scan history for current user | Yes |
| GET | `/api/scans/analytics` | Get scan analytics and stats | Yes |

## How It Works

1. User uploads a video via the web interface
2. Backend extracts frames using **OpenCV**
3. Frames are passed through a **TensorFlow** deepfake detection model
4. **LIME** generates visual explanations highlighting suspicious regions
5. Results are stored based on auth state:
   - **Anonymous users:** temporary local files (auto-cleaned)
   - **Authenticated users:** persisted to **Supabase cloud storage**
6. Scan results saved to **PostgreSQL** for history and analytics

## Security

- Passwords hashed with **Argon2** via Passlib
- Routes protected with **JWT middleware**
- UUID-based file naming prevents collisions and path traversal
- Automatic cleanup of temporary files prevents orphaned storage
