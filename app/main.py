from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI
from database import test_connection

app = FastAPI()

class Command(BaseModel):
    action: str

origins = [
#    "http://localhost:3000",
#    "http://192.168.255.219:3000",
    "https://oleksandrlozenko.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/toggle")
async def toggle_light(command: Command):
    if command.action == "on":
        print("Лампочка включена")
        return {"message": "Лампочка включена"}
    elif command.action == "off":
        print("Лампочка выключена")
        return {"message": "Лампочка выключена"}
    else:
        raise HTTPException(status_code=400, detail="Неверная команда")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.on_event("startup")
async def startup():
    await test_connection()
