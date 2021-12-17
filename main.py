import pandas as pd
import db_operations as db


if __name__ == '__main__':
    branches       = pd.read_csv("branches.csv")
    departments    = pd.read_csv("departments.csv")
    employees      = pd.read_csv("employees.csv")
    applications   = pd.read_csv("applications.csv")
    business_trips = pd.read_csv("business_trips.csv")

    # Заполнение базы данных
    db.insert_branches(branches)
    db.insert_departments(departments)
    db.insert_employees(employees)
    db.insert_applications(applications)
    db.insert_business_trips(business_trips)