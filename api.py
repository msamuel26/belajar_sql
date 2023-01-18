from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, Field
from sqlalchemy.ext.declarative import declarative_base
from fastapi.responses import JSONResponse


app = FastAPI()

# Connect to the PostgreSQL database
engine = create_engine('postgresql://postgres:postgres@localhost:5432/api', echo=True)
Base = declarative_base()

# Create a Pydantic model for the User
class UserCreate(BaseModel):
    name: str = Field(..., example="John Doe")
    age: int = Field(..., example=25)

# Create a SQLAlchemy model for the User
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)

# Create the "users" table in the database
Base.metadata.create_all(bind=engine)

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a route to create a new user in the database
@app.post("/users/") 
async def create_user(user: UserCreate):
    session = SessionLocal()
    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    session.close()
    return {"message": "User created successfully"}

# Define a route to list all users from the database
@app.get("/users/", response_class=JSONResponse)
async def list_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return JSONResponse(content= [{"id": user.id, "name": user.name, "age": user.age} for user in users])

@app.get("/")
async def root():
    return {"message": "Hello World"}