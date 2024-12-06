from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from colorama import init, Fore, Style

init(autoreset=True)

app = FastAPI()

Base = declarative_base()

# Определение модели пользователя
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True)
    password = Column(String)  # Пароли хранятся в зашифрованном виде
    data_create = Column(DateTime)
    updated_at = Column(DateTime)
    role_id = Column(Integer)
    email = Column(String, index=True)
    status = Column(Boolean)

# Класс Command для команд управления устройством
class Command(BaseModel):
    action: str

DATABASE_URL = "mysql+aiomysql://root:@localhost/sh_db"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Зависимость для получения сессии базы данных
async def get_db_session():
    async with SessionLocal() as session:
        yield session

# API-эндпоинт для чтения всех пользователей
@app.get("/users")
async def read_users(db: AsyncSession = Depends(get_db_session)):
    async with db as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        users_data = [
            {
                "user_id": user.user_id,
                "login": user.login,
                "password": str(user.password),
                "data_create": str(user.data_create),
                "updated_at": str(user.updated_at),
                "role_id": user.role_id,
                "email": user.email,
                "status": user.status
            } for user in users if user
        ]
        
        # Проверяем, что users_data является массивом (списком)
        if not isinstance(users_data, list):
            raise HTTPException(status_code=500, detail="Ошибка на сервере: данные пользователей не являются массивом")
        
        # Выводим данные в консоль с использованием цветного форматирования
        print(f"{Fore.RED}{Style.BRIGHT}Sending user data: {users_data}")

        return users_data


# API-эндпоинт для управления устройством
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

# Простой эндпоинт для проверки здоровья сервиса
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Настройка CORS для обработки запросов из фронтенда
origins = ["http://localhost:3000", "https://oleksandrlozenko.github.io"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для примера разрешены все источники
    allow_methods=["*"],
    allow_headers=["*"]
)