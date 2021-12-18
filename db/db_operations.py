from db.db_auth import conn, psycopg2
from random import randint
from _datetime import datetime


# Добавление данных о филиалах
def insert_branches(branches):
    rows_len = branches.shape[0]

    for i in range(rows_len):
        branch = branches.loc[[i]].to_dict()

        branch_name = branch['branch_name'][i]
        branch_num  = branch['branch_num'][i]
        country     = branch['country'][i]
        region      = ''.join(branch['region'][i].split("'"))
        location    = ''.join(branch['location'][i].split("'"))
        street      = branch['street'][i]
        building    = branch['building'][i]
        housing     = branch['housing'][i]

        country_id  = 0
        region_id   = 0
        location_id = 0

        # Добавление данных о стране
        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO countries (country_name) VALUES (%s)",
                                (country,))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

        with conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT country_id FROM countries WHERE country_name='{country}'")
                country_id = cur.fetchone()[0]

        # Добавление данных о регионе
        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO regions (country_id, region_name) VALUES (%s, %s)",
                                (country_id, region))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

        with conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT region_id FROM regions WHERE country_id={country_id} AND region_name='{region}'")
                region_id = cur.fetchone()[0]

        # Добавление данных о населенном пункте
        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO locations (region_id, location_name) VALUES (%s, %s)",
                                (region_id, location))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

        with conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT location_id FROM locations "
                            f"WHERE region_id={region_id} AND location_name='{location}'")
                location_id = cur.fetchone()[0]

        # Добавление данных об адресе филиала
        address_id = 0
        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO branches_addresses (location_id, street, building, housing)"
                                " VALUES (%s, %s, %s, %s)",
                                (location_id, street, building, housing))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

        with conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT address_id FROM branches_addresses "
                            f"WHERE location_id={location_id} AND street='{street}' AND"
                            f"      building={building} AND housing={housing}")
                address_id = cur.fetchone()[0]

        # Добавление данных об филиале
        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO branches (branch_name, branch_num, address_id)"
                                " VALUES (%s, %s, %s)",
                                (branch_name, branch_num, address_id))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

    return


# Добавление данных о подразделениях
def insert_departments(departments):
    rows_len = departments.shape[0]

    for i in range(rows_len):
        department = departments.loc[[i]].to_dict()

        department_name = department['department_name'][i]

        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO departments (department_name)"
                                " VALUES (%s)",
                                (department_name,))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

    return


# Добавление данных о сотрудниках
def insert_employees(employees):
    rows_len = employees.shape[0]

    for i in range(rows_len):
        employee = employees.loc[[i]].to_dict()

        name_and_patronymic = employee['name'][i] + ' ' + employee['patronymic'][i]
        surname    = employee['surname'][i]
        birthday   = employee['birthday'][i]

        login      = employee['login'][i]
        password   = employee['password'][i]

        responsibilities = employee['responsibilities'][i]
        state      = employee['state'][i]
        branch_id  = employee['branch_id'][i]

        passport_series = employee['passport_series'][i]
        passport_num = employee['passport_num'][i]
        issued_by  = employee['issued_by'][i]
        issue_date = employee['issue_date'][i]
        country    = employee['country'][i]
        region     = ''.join(employee['region'][i].split("'"))
        location   = ''.join(employee['location'][i].split("'"))

        phone_number1 = employee['phone_number1'][i]
        phone_number2 = employee['phone_number2'][i]
        phone_number3 = employee['phone_number3'][i]

        # Добавление данных о месте рождения
        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO countries (country_name) VALUES (%s)",
                                (country,))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

        with conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT country_id FROM countries WHERE country_name='{country}'")
                country_id = cur.fetchone()[0]

        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO regions (country_id, region_name) VALUES (%s, %s)",
                                (country_id, region))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

        with conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT region_id FROM regions WHERE country_id={country_id} AND region_name='{region}'")
                region_id = cur.fetchone()[0]

        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO locations (region_id, location_name) VALUES (%s, %s)",
                                (region_id, location))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

        with conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT location_id FROM locations "
                            f"WHERE region_id={region_id} AND location_name='{location}'")
                location_id = cur.fetchone()[0]

        # Добавление данных паспорта
        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO passports (passport_series, passport_num, issued_by, issue_date, "
                                "location_id) "
                                "VALUES (%s, %s, %s, %s, %s)",
                                (passport_series, passport_num, issued_by, issue_date, location_id))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

        with conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT passport_id FROM passports "
                            f"WHERE passport_series={passport_series} AND passport_num={passport_num}")
                passport_id = cur.fetchone()[0]

        # Добавление данных о сотруднике
        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO employees (name_and_patronymic, surname, birthday, responsibilities, "
                                "state, branch_id, passport_id) "
                                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                (name_and_patronymic, surname, birthday, responsibilities, state, branch_id,
                                 passport_id))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

        with conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT employee_id FROM employees "
                            f"WHERE passport_id={passport_id}")
                employee_id = cur.fetchone()[0]

        # Добавление данных об учетной записи сотрудника
        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO account_data (login, password, employee_id)"
                                "VALUES (%s, %s, %s)",
                                (login, password, employee_id))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

        # Добавление данных о контактных номерах сотрудника
        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO phone_numbers (phone_num, employee_id)"
                                "VALUES (%s, %s)",
                                (phone_number1, employee_id))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO phone_numbers (phone_num, employee_id)"
                                "VALUES (%s, %s)",
                                (phone_number2, employee_id))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO phone_numbers (phone_num, employee_id)"
                                "VALUES (%s, %s)",
                                (phone_number3, employee_id))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

        # Определение подразделений для сотрудника (произвольно)
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT department_id FROM departments")
                department_ids = cur.fetchall()
                len_deph = len(department_ids)
                department_id = department_ids[randint(0, len_deph - 1)]

        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO employee_department (employee_id, department_id)"
                                "VALUES (%s, %s)",
                                (employee_id, department_id))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

    return


# Добавление данных о заявлениях
def insert_applications(applications):
    rows_len = applications.shape[0]

    for i in range(rows_len):
        application = applications.loc[[i]].to_dict()

        application_type = application['application_type'][i]
        status           = application['status'][i]
        application_date = application['application_date'][i].split(' ')[0]
        application_time = application['application_time'][i]
        solution_date    = application['solution_date'][i].split(' ')[0]
        solution_time    = application['solution_time'][i]
        date_start       = application['date_start'][i].split(' ')[0]
        date_finish      = application['date_finish'][i].split(' ')[0]
        applicant_id     = int(application['applicant_id'][i])

        # Определение согласовавшего лица (произвольно)
        solver_id = 0
        if status != 'in process':
            solver_id = randint(1, 300)
            while applicant_id == solver_id:
                solver_id = randint(1, 300)

        # Конкатенация даты и времени подачи заявления
        # Аналогично для даты рассмотрения заявления
        application_date = application_date + " " + application_time
        try:
            solution_date = (solution_date + " " + solution_time)
        except:
            solution_date = None

        # Добавление данных заявления
        with conn:
            try:
                with conn.cursor() as cur:
                    if status == 'in process':
                        cur.execute("INSERT INTO applications (application_type, status, application_date, "
                                    "solution_date, date_start, date_finish, applicant_id) "
                                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                    (application_type, status, application_date, solution_date, date_start, date_finish,
                                     applicant_id))
                    else:
                        cur.execute( "INSERT INTO applications (application_type, status, application_date, "
                                     "solution_date, date_start, date_finish, applicant_id, solver_id) "
                                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                     (application_type, status, application_date, solution_date, date_start,
                                      date_finish, applicant_id, solver_id))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

    return


# Добавление данных о командировках
def insert_business_trips(business_trips):
    rows_len = business_trips.shape[0]

    for i in range(rows_len):
        business_trip = business_trips.loc[[i]].to_dict()

        application_id = business_trip['application_id'][i]
        branch_id      = business_trip['branch_id'][i]
        instruction    = business_trip['instruction'][i]
        employee_id    = business_trip['employee_id'][i]

        with conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO business_trips (application_id, branch_id, instruction, employee_id)"
                                "VALUES (%s, %s, %s, %s)",
                                (application_id, branch_id, instruction, employee_id))
            except psycopg2.errors.UniqueViolation as error:
                print("Error time: ", datetime.now(), ", Message: ", error)

    return