from dataclasses import dataclass
from datetime import date
import database
@dataclass(frozen=True) # this is a dataclass meaning that the class can be defined using init and frozen=true meanings this is a read only class
class Transaction():
    day:date
    kind:str #this will represent if it is a expense or saving
    amount:int #representing PKR always positive
    one_off:bool=False #big one time expense seems kinda unneccesary but you never know
def balance(start_amount:int,transactions:list[Transaction]): #make transactions as a list of the class Transaction
    spent=sum(t.amount for t in transactions if t.kind =="expense") # for amount in the list check if that kind is expense
    saved= sum(t.amount for t in transactions if t.kind=="saving") # same thing
    return start_amount + saved - spent

def total_saved(transactions): #returns total money saved
    return sum(t.amount for t in transactions if t.kind == "saving")


def spend_rate(transactions, today): #calculates and projects spend rate based on recent activity
    spent = sum(t.amount for t in transactions
                if t.kind == "expense" and not t.one_off and t.day <= today)
    return spent / today.day
import calendar
def project(start_amount:int,transactions:list[Transaction],today:date):
    current=balance(start_amount,transactions) #gets balance
    rate=spend_rate(transactions,today) #gets spend rate
    days_month=calendar.monthrange(today.year,today.month)[1] #gets days in month
    days_left=days_month - today.day #gets days left in the month
    return current-rate*days_left #calculates projected outcome and balance

