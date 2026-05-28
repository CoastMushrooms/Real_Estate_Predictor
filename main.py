import pickle
import sqlite3
import threading, webbrowser
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

def init_db():
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sqft INTEGER,
            beds INTEGER,
            predicted_price REAL
        )
    """)
    conn.commit()
    conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    threading.Timer(1.0, lambda: webbrowser.open("http://localhost:8000")).start()
    yield

app = FastAPI(lifespan=lifespan)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r") as f:
        return f.read()

@app.get("/predict")
def predict(sqft: int, beds: int):
    prediction = model.predict([[sqft, beds]])
    final_price = round(float(prediction[0][0]), 2)

    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (sqft, beds, predicted_price) VALUES (?, ?, ?)",
        (sqft, beds, final_price),
    )
    conn.commit()
    conn.close()

    return {
        "requested_sqft": sqft,
        "requested_beds": beds,
        "estimated_price": final_price,
    }

@app.get("/history")
def get_history():
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": r[0], "sqft": r[1], "beds": r[2], "predicted_price": r[3]}
        for r in rows
    ]