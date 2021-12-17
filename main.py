import pandas as pd
from db import db_operations as db

if __name__ == '__main__':
    branches       = pd.read_csv("data/branches.csv")
    departments    = pd.read_csv("data/departments.csv")
    employees      = pd.read_csv("data/employees.csv")
    applications   = pd.read_csv("data/applications.csv")
    business_trips = pd.read_csv("data/business_trips.csv")

    # Заполнение базы данных
    db.insert_branches(branches)
    db.insert_departments(departments)
    db.insert_employees(employees)
    db.insert_applications(applications)
    db.insert_business_trips(business_trips)