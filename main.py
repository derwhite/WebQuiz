from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uuid
import random
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:5500",
    "http://localhost:8080",
    "http://deine-domain.de",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # für Entwicklung ok
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}


# --- Datenmodell ---
class Answer(BaseModel):
    question_id: int
    selected_option: int


# --- Dummy-Fragen (später Datenbank) ---
questions = [
    {
        "id": 1,
        "question": "Was ist die Hauptstadt von Deutschland?",
        "options": ["Berlin", "Paris", "Madrid", "Rom"],
        "correct_option": 0,
        "explanation": "Berlin ist seit 1990 die Hauptstadt des wiedervereinigten Deutschlands.",
    },
    {
        "id": 2,
        "question": "Wie viel ist 5 + 7?",
        "options": ["10", "11", "12", "13"],
        "correct_option": 2,
        "explanation": "5 + 7 ergibt 12, weil Addition die Summe zweier Zahlen bildet.",
    },
]


# --- Endpunkte ---


@app.get("/question")
def get_question(session_id: str = Query(None)):
    # Neue Session erstellen falls keine existiert
    if not session_id:
        session_id = str(uuid.uuid4())
        sessions[session_id] = []

    question = random.choice(questions)
    return {
        "id": question["id"],
        "question": question["question"],
        "options": question["options"],
        "session_id": session_id,
    }


@app.post("/answer")
def check_answer(answer: Answer):
    question = next((q for q in questions if q["id"] == answer.question_id), None)

    if not question:
        raise HTTPException(status_code=404, detail="Frage nicht gefunden")

    is_correct = question["correct_option"] == answer.selected_option

    return {
        "correct": is_correct,
        "correct_option": question["correct_option"],
        "explanation": question["explanation"],
    }
