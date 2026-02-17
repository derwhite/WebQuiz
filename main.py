from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uuid
import random
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

sessions = {}
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


# --- Datenmodell ---
class Answer(BaseModel):
    question_id: int
    selected_option: int


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
    {
        "id": 3,
        "question": "Welcher Planet ist der Sonne am nächsten?",
        "options": ["Venus", "Mars", "Merkur", "Jupiter"],
        "correct_option": 2,
        "explanation": "Merkur ist der innerste Planet unseres Sonnensystems und der Sonne am nächsten.",
    },
    {
        "id": 4,
        "question": "Wie viele Kontinente gibt es auf der Erde?",
        "options": ["5", "6", "7", "8"],
        "correct_option": 2,
        "explanation": "Es gibt sieben Kontinente: Europa, Asien, Afrika, Nordamerika, Südamerika, Australien und Antarktis.",
    },
    {
        "id": 5,
        "question": "Wie viel ist 9 x 8?",
        "options": ["72", "81", "64", "70"],
        "correct_option": 0,
        "explanation": "9 mal 8 ergibt 72.",
    },
    {
        "id": 6,
        "question": "Welches Gas atmen Menschen hauptsächlich ein?",
        "options": ["Sauerstoff", "Kohlenstoffdioxid", "Stickstoff", "Helium"],
        "correct_option": 0,
        "explanation": "Menschen benötigen Sauerstoff zum Atmen und zur Energiegewinnung im Körper.",
    },
    {
        "id": 7,
        "question": "Wer schrieb 'Faust'?",
        "options": ["Friedrich Schiller", "Johann Wolfgang von Goethe", "Thomas Mann", "Bertolt Brecht"],
        "correct_option": 1,
        "explanation": "'Faust' wurde von Johann Wolfgang von Goethe geschrieben.",
    },
    {
        "id": 8,
        "question": "Wie viele Minuten hat eine Stunde?",
        "options": ["50", "55", "60", "65"],
        "correct_option": 2,
        "explanation": "Eine Stunde besteht aus 60 Minuten.",
    },
    {
        "id": 9,
        "question": "Welches Element hat das chemische Symbol 'O'?",
        "options": ["Gold", "Osmium", "Sauerstoff", "Silber"],
        "correct_option": 2,
        "explanation": "Das chemische Symbol 'O' steht für Sauerstoff.",
    },
    {
        "id": 10,
        "question": "In welchem Land stehen die Pyramiden von Gizeh?",
        "options": ["Mexiko", "Peru", "Ägypten", "Indien"],
        "correct_option": 2,
        "explanation": "Die berühmten Pyramiden von Gizeh befinden sich in Ägypten.",
    },
    {
        "id": 11,
        "question": "Wie viel ist die Quadratwurzel von 81?",
        "options": ["7", "8", "9", "10"],
        "correct_option": 2,
        "explanation": "Die Quadratwurzel von 81 ist 9, da 9 × 9 = 81.",
    },
    {
        "id": 12,
        "question": "Welches Meer liegt zwischen Europa und Afrika?",
        "options": ["Ostsee", "Nordsee", "Mittelmeer", "Schwarzes Meer"],
        "correct_option": 2,
        "explanation": "Das Mittelmeer trennt Europa und Afrika geografisch.",
    },
    {
        "id": 13,
        "question": "Wie viele Bundesländer hat Deutschland?",
        "options": ["14", "15", "16", "17"],
        "correct_option": 2,
        "explanation": "Deutschland besteht aus 16 Bundesländern.",
    },
    {
        "id": 14,
        "question": "Welches Instrument hat typischerweise 88 Tasten?",
        "options": ["Gitarre", "Klavier", "Violine", "Flöte"],
        "correct_option": 1,
        "explanation": "Ein Klavier besitzt in der Regel 88 Tasten.",
    },
    {
        "id": 15,
        "question": "Wie viel ist 15 - 4?",
        "options": ["9", "10", "11", "12"],
        "correct_option": 2,
        "explanation": "15 minus 4 ergibt 11.",
    },
    {
        "id": 16,
        "question": "Welcher Ozean ist der größte der Erde?",
        "options": ["Atlantischer Ozean", "Indischer Ozean", "Arktischer Ozean", "Pazifischer Ozean"],
        "correct_option": 3,
        "explanation": "Der Pazifische Ozean ist der größte Ozean der Erde.",
    },
    {
        "id": 17,
        "question": "Wie viele Sekunden hat eine Minute?",
        "options": ["30", "45", "60", "90"],
        "correct_option": 2,
        "explanation": "Eine Minute besteht aus 60 Sekunden.",
    },
    {
        "id": 18,
        "question": "Wer malte die Mona Lisa?",
        "options": ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Claude Monet"],
        "correct_option": 1,
        "explanation": "Die Mona Lisa wurde von Leonardo da Vinci gemalt.",
    },
    {
        "id": 19,
        "question": "Wie viele Tage hat ein Schaltjahr?",
        "options": ["365", "366", "364", "367"],
        "correct_option": 1,
        "explanation": "Ein Schaltjahr hat 366 Tage, da der Februar einen zusätzlichen Tag erhält.",
    },
    {
        "id": 20,
        "question": "Welches Tier wird oft als 'König der Tiere' bezeichnet?",
        "options": ["Tiger", "Elefant", "Löwe", "Adler"],
        "correct_option": 2,
        "explanation": "Der Löwe wird traditionell als 'König der Tiere' bezeichnet.",
    },
    {
        "id": 21,
        "question": "Wie viel ist 100 durch 4?",
        "options": ["20", "25", "30", "40"],
        "correct_option": 1,
        "explanation": "100 geteilt durch 4 ergibt 25.",
    },
    {
        "id": 22,
        "question": "Welche Farbe entsteht durch die Mischung von Blau und Gelb?",
        "options": ["Rot", "Grün", "Lila", "Orange"],
        "correct_option": 1,
        "explanation": "Blau und Gelb ergeben gemischt die Farbe Grün.",
    },
]


# --- Endpunkte ---
@app.get("/question")
def get_question(session_id: str = Query(None)):

    # Neue Session erstellen falls keine existiert
    if not session_id:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {"date": datetime.now() + timedelta(minutes=30), "played": set()}

    exp_sess = [k for k, v in sessions.items() if v["date"] <= datetime.now()]
    for i in exp_sess:
        del sessions[i]

    question = random.choice(questions)
    while question["id"] in sessions[session_id]["played"]:
        if len(questions) == len(sessions[session_id]["played"]):
            return {
                "id": 9999,
                "question": "kein Fragen mehr",
                "options": ["Error", "Error"],
                "session_id": session_id,
            }
        question = random.choice(questions)

    sessions[session_id]["played"].add(question["id"])
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
