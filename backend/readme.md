# SIH26001 — Landslide Early-Warning Backend Service

FastAPI-powered REST API backend for live landslide risk assessment, spatial risk monitoring, citizen report logging, and integration with the trained AI model.

## Features
- **Live Model Inference**: POST `/api/v1/predict` receives location and environmental metrics, calls the `ai/` XGBoost model, and returns risk probability, risk score, and risk category.
- **Citizen Landslide Reports**: Submit (`POST /api/v1/reports`) and query (`GET /api/v1/reports`) crowd-sourced landslide observations.
- **Database Logging**: Automatically logs all spatial risk predictions and citizen reports to database (supports SQLite for local dev & PostgreSQL/PostGIS for production).
- **Health Diagnostics**: GET `/api/v1/health` checks database connectivity and loaded model state.

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Server Locally**:
   ```bash
   python -m uvicorn app.main:app --reload --port 8000
   ```

3. **Interactive API Documentation (Swagger UI)**:
   Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

4. **Run Unit & Integration Tests**:
   ```bash
   pytest tests/
   ```