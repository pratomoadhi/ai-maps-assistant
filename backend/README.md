# 🗺️ Maps Assistant Backend

A FastAPI backend that connects to **OpenStreetMap (Nominatim)** and **OpenRouteService** to provide:

* 🔍 Place search (`/places`)
* 🛣️ Driving directions (`/directions`)
* 🏓 Health check (`/ping`)

This service is designed to integrate with **Open WebUI** as tools, but can also be used standalone.

---

## 📂 Project Structure

```
backend/
│── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI entrypoint
│   ├── routes.py       # Endpoints (/ping, /places, /directions)
│   └── utils.py        # Helper functions for OSM + ORS
│
│── requirements.txt    # Dependencies
│── README.md           # This file
```

---

## 🚀 Setup & Run

### 1. Clone Repo

```bash
git clone https://github.com/<your-username>/my-maps-assistant.git
cd my-maps-assistant/backend
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate it:

* **Linux / Mac**

  ```bash
  source .venv/bin/activate
  ```
* **Windows (PowerShell)**

  ```powershell
  .venv\Scripts\Activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in `backend/` with your OpenRouteService API key:

```env
ORS_API_KEY=your_openrouteservice_key
```

You can get a free ORS key from: [https://openrouteservice.org/sign-up](https://openrouteservice.org/sign-up)

### 5. Run the Server

```bash
uvicorn app.main:app --reload
```

Server runs at:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔎 API Endpoints

### Health Check

```http
GET /ping
```

Response:

```json
{"status": "ok"}
```

### Place Search

```http
GET /places?query=restaurant jakarta
```

Response (example):

```json
[
  {
    "place_id": "123",
    "display_name": "Restaurant, Jakarta, Indonesia",
    "lat": "-6.2",
    "lon": "106.8"
  }
]
```

### Driving Directions

```http
GET /directions?origin=106.8272,-6.1754&destination=106.8140,-6.1352
```

Response: JSON route object from OpenRouteService.

---

## 🧰 Development Notes

* Virtual environment is inside `backend/.venv/` (excluded from Git).
* Dependencies tracked in `requirements.txt`.
* API keys and secrets should go in `.env` (excluded from Git).
* This backend is designed to be extended with more endpoints (e.g. transit, walking).

---

## 📜 License

MIT
