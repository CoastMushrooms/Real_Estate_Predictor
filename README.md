# Real Estate ML Price Predictor
 
A full-stack machine learning application that scrapes property listings, trains a linear regression model, and serves real-time price predictions through a REST API with a browser-based UI. The server auto-opens the app in your browser on startup.
 
---
 
## Features
 
- **Web Scraper** — parses property listings from HTML using BeautifulSoup, with a live book scraper from `books.toscrape.com`
- **ML Model** — trains a Linear Regression model on sqft and bedroom count to predict prices
- **REST API** — FastAPI backend with `/predict` and `/history` endpoints
- **Frontend UI** — clean browser interface to input property details and get instant estimates
- **Auto-launch** — server automatically opens `http://localhost:8000` in your browser on startup
- **Persistent Storage** — all predictions are logged to a local SQLite database
---
 
## Tech Stack
 
| Layer | Technology |
|---|---|
| Scraping | Python, BeautifulSoup, Requests |
| Data | Pandas, CSV |
| ML | scikit-learn (LinearRegression) |
| API | FastAPI, Uvicorn |
| Storage | SQLite |
| Frontend | HTML, CSS, Vanilla JS |
 
---
 
## Project Structure
 
```
real_estate-ml/
├── mock_listings.html   # 200 property listings used as scraping source
├── scraper.py           # Scrapes mock listings → data.csv; also scrapes live books
├── real_scraper.py      # Standalone live book scraper (books.toscrape.com)
├── train_model.py       # Trains model on data.csv → model.pkl
├── main.py              # FastAPI server — loads model, serves predictions, auto-opens browser
├── index.html           # Frontend UI
├── data.csv             # Scraped training data (generated, do not edit manually)
├── model.pkl            # Serialized trained model (generated)
├── predictions.db       # SQLite database of prediction history (generated)
├── requirements.txt     # Python dependencies
└── .gitignore           # Excludes venv and generated files from git
```
 
---
 
## Setup & Usage
 
### 1. Clone the repo and create a virtual environment
 
```bash
git clone https://github.com/yourusername/real_estate-ml.git
cd real_estate-ml
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux
```
 
### 2. Install dependencies
 
```bash
pip install -r requirements.txt
```
 
### 3. Run the full pipeline
 
```bash
# Step 1 — scrape listings into data.csv
python scraper.py
 
# Step 2 — train the model
python train_model.py
 
# Step 3 — start the server (auto-opens browser)
uvicorn main:app --reload
```
 
The app will automatically open at **http://localhost:8000** in your browser.
 
---
 
## API Endpoints
 
### `GET /predict`
Returns a price estimate for a given property.
 
**Query params:** `sqft` (int), `beds` (int)
 
```
GET /predict?sqft=1500&beds=3
```
 
```json
{
  "requested_sqft": 1500,
  "requested_beds": 3,
  "estimated_price": 387500.0
}
```
 
---
 
### `GET /history`
Returns all past predictions from the database, newest first.
 
```json
[
  { "id": 3, "sqft": 1500, "beds": 3, "predicted_price": 387500.0 },
  { "id": 2, "sqft": 900,  "beds": 2, "predicted_price": 241000.0 }
]
```
 
---
 
## Model Details
 
- **Algorithm:** Linear Regression
- **Features:** `sqft`, `beds`
- **Target:** `price`
- **Training data:** 200 synthetically generated property listings
- **Serialization:** `pickle`
---

## Railway Link

** Link: realestatepredictor-production.up.railway.app
