from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, Field
from sqlalchemy.ext.declarative import declarative_base
from fastapi.responses import JSONResponse


app = FastAPI()

# Connect to the PostgreSQL database
engine = create_engine('postgresql://postgres:postgres@localhost:5432/api2', echo=True)
Base = declarative_base()

# Create a Pydantic model for the Customer
class CustomerCreate(BaseModel):
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    age: int = Field(..., example=23)
    country: str = Field(..., example='USA')

# Create a Pydantic model for the Order
class OrderCreate(BaseModel):
    item: str = Field(..., example="Keyboard")
    amount: int = Field(..., example=300)
    customer_id: int = Field(..., example=1)

# Create a Pydantic model for the Shipping
class ShippingCreate(BaseModel):
    status: str = Field(..., example='Pending')
    customer: int = Field(..., example=3)

# Create a SQLAlchemy model for the Customer
class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    country = Column(String)

# Create a SQLAlchemy model for the Order
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String)
    amount = Column(Integer)
    customer_id = Column(Integer)

# Create a SQLAlchemy model for the Order
class Shipping(Base):
    __tablename__ = 'shippings'
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    customer_id = Column(Integer)

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

# Define a route to create a new order in the database
@app.post("/orders/") 
async def create_order(order: OrderCreate):
    session = SessionLocal()
    new_order = Order(**order.dict())
    session.add(new_order)
    session.commit()
    session.close()
    return {"message": "Order created successfully"}

# Define a route to create a new shipping in the database
@app.post("/shippings/") 
async def create_shipping(shipping: ShippingCreate):
    session = SessionLocal()
    new_shipping = Shipping(**shipping.dict())
    session.add(new_shipping)
    session.commit()
    session.close()
    return {"message": "Shipping created successfully"}

# Define a route to list all customers from the database
@app.get("/customers/", response_class=JSONResponse)
async def list_customers():
    session = SessionLocal()
    customers = session.query(Customer).all()
    session.close()
    return JSONResponse(content= [{"id": customer.id, "first_name": customer.first_name, "last_name": customer.last_name, "age": customer.age, "country": customer.country} for customer in customers])

# Define a route to list all orders from the database
@app.get("/orders/", response_class=JSONResponse)
async def list_orders():
    session = SessionLocal()
    orders = session.query(Order).all()
    session.close()
    return JSONResponse(content= [{"id": order.id, "item": order.item, "amount": order.amount, "customer_id": order.customer_id} for order in orders])

# Define a route to list all shippings from the database
@app.get("/shippings/", response_class=JSONResponse)
async def list_shippings():
    session = SessionLocal()
    shippings = session.query(Order).all()
    session.close()
    return JSONResponse(content= [{"id": shipping.id, "status": shipping.status, "customer_id": shipping.customer_id} for shipping in shippings])

@app.get("/")
async def root():
    return {"message": "Hello Customer"}
