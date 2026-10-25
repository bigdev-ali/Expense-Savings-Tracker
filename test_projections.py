from datetime import date
from projections import Transaction, balance, spend_rate, project

TODAY = date(2026, 11, 3) #this is a sample test file each function begins with test and assert means something which is true or false 

TXNS = [
    Transaction(date(2026, 11, 1), "expense", 100),
    Transaction(date(2026, 11, 2), "expense", 100),
    Transaction(date(2026, 11, 3), "expense", 700),
    Transaction(date(2026, 11, 2), "saving", 2000),
]


def test_balance():
    assert balance(30000, TXNS) == 31100


def test_spend_rate_ignores_savings():
    assert spend_rate(TXNS, TODAY) == 300


def test_project():
    assert project(30000, TXNS, TODAY) == 23000


def test_no_transactions_projects_starting_amount():
    assert project(30000, [], TODAY) == 30000