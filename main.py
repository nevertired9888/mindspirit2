from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI(title="MindSprint Quiz")

BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Настройка Jinja2 с правильными настройками
templates = Jinja2Templates(directory=BASE_DIR / "templates")

QUESTIONS = [
    {
        "id": 1,
        "category": "Наука",
        "question": "Какая планета Солнечной системы самая большая?",
        "options": ["Сатурн", "Марс", "Юпитер", "Нептун"],
        "correct": 2
    },
    {
        "id": 2,
        "category": "История",
        "question": "Как звали первого космонавта, полетевшего в космос?",
        "options": ["Нил Армстронг", "Юрий Гагарин", "Алексей Леонов", "Герман Титов"],
        "correct": 1
    },
    {
        "id": 3,
        "category": "Спорт",
        "question": "Как называется игра с мячом, в которой его нужно забросить в кольцо?",
        "options": ["Волейбол", "Баскетбол", "Гандбол", "Теннис"],
        "correct": 1
    },
    {
        "id": 4,
        "category": "Музыка",
        "question": "Какой инструмент называют «королём» из-за размеров и звучания?",
        "options": ["Гитара", "Флейта", "Орган", "Барабан"],
        "correct": 2
    },
    {
        "id": 5,
        "category": "Игры",
        "question": "В какой игре нужно строить из кубиков?",
        "options": ["Minecraft", "Tetris", "Roblox", "Fortnite"],
        "correct": 0
    }
]

user_answers = {}

@app.get("/", response_class=HTMLResponse)
async def get_quiz(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "questions": QUESTIONS,
            "categories": ["Наука", "История", "Спорт", "Музыка", "Игры"]
        }
    )

@app.post("/submit", response_class=HTMLResponse)
async def submit_answer(request: Request, question_id: int = Form(...), answer: int = Form(...)):
    user_answers[question_id] = answer
    correct_count = sum(1 for q in QUESTIONS if user_answers.get(q["id"]) == q["correct"])
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "questions": QUESTIONS,
            "categories": ["Наука", "История", "Спорт", "Музыка", "Игры"],
            "user_answers": user_answers,
            "show_results": True,
            "correct_count": correct_count,
            "total": len(QUESTIONS)
        }
    )

@app.post("/reset")
async def reset_quiz():
    user_answers.clear()
    return {"status": "ok"}