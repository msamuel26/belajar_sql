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

# Create a Pydantic model for the Customer
class CustomerCreate(BaseModel):
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    age: int = Field(..., example=23)
    country: str = Field(..., example='USA')

# Create a SQLAlchemy model for the User
class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    country = Column(String)

# Create the "users" table in the database
Base.metadata.create_all(bind=engine)

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a route to create a new customer in the database
@app.post("/customers/") 
async def create_customer(customer: CustomerCreate):
    session = SessionLocal()
    new_customer = Customer(**customer.dict())
    session.add(new_customer)
    session.commit()
    session.close()
    return {"message": "Customer created successfully"}

# Define a route to list all customers from the database
@app.get("/customers/", response_class=JSONResponse)
async def list_customers():
    session = SessionLocal()
    customers = session.query(Customer).all()
    session.close()
    return JSONResponse(content= [{"id": customer.id, "first_name": customer.first_name, "last_name": customer.last_name, "age": customer.age, "country": customer.country} for customer in customers])

@app.get("/")
async def root():
    return {"message": "Hello Customer"}
