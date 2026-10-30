from fastapi import FastAPI
from pydantic import BaseModel, Field

from database import connect, set_starting_amount

app = FastAPI()

class MonthIn(BaseModel): #MonthIn describes what a valid request looks like it's a pydantic model where each field has a type and rules
    month: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$") #the pattern for month as four digits a dash and from 0-12 
    amount: int = Field(ge=0) #amount must be an int and it should be greater than or equals to zero


@app.get("/") #it is a decorator which means that whenever get is called it runs this function
def home():
    return {"message": "expense tracker is alive"} #this returns a python dictionary


@app.post("/months") #decorator for when post is called run this function and sends data back to the server
def set_month(body: MonthIn): # tells fastapi to check the request's json and check it against month in if valid return a clean object else it will raise a error automatically
    conn = connect() #opens a database connect
    set_starting_amount(conn, body.month, body.amount)
    conn.close()
    return {"month": body.month, "starting_amount": body.amount} #returns a dictionary according to the values in the database in the starting amount for the month