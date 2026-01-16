from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from prompt import SYSTEM_PROMPT

load_dotenv()

client = OpenAI()

app = FastAPI(title="İslami Hoca AI", version="1.0")

class Question(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "İslami Hoca AI çalışıyor"}

@app.post("/ask")
async def ask_hoca(data: Question):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": data.question}
        ],
        temperature=0.3
    )

    return {
        "answer": completion.choices[0].message.content,
        "disclaimer": "Bu cevap bilgilendirme amaçlıdır. Kesin dini hüküm için ehil bir âlime danışınız."
    }
