drop table if exists business_trips;
drop table if exists applications;

drop table if exists account_data;
drop table if exists phone_numbers;

drop table if exists employee_department;
drop table if exists departments;

drop table if exists employees;
drop table if exists passports;

drop table if exists branches;
drop table if exists branches_addresses;

drop table if exists locations;
drop table if exists regions;
drop table if exists countries;


--------------------------------------------------------------

-- Addresses

create table countries (
	country_id   SERIAL,
	country_name VARCHAR(150) not null unique,
	primary key (country_id) 
);

create table regions (
	region_id   SERIAL,
	country_id  INT not null,
	region_name VARCHAR(150) not null,
	unique (country_id, region_name),
	primary key (region_id),
	foreign key (country_id) references countries (country_id) 
);

create table locations (
	location_id SERIAL,
	region_id   INT not null,
	location_name VARCHAR(150) not null,
	unique (region_id, location_name),
	primary key (location_id),
	foreign key (region_id) references regions (region_id)
);

--------------------------------------------------------------

-- Branches

create table branches_addresses (
	address_id  SERIAL,
	location_id INT    not null,
	street      VARCHAR(50) not null,
	building    INT    not null check (building > 0),
	housing     INT    not null default 0,
	unique (location_id, street, building, housing),
	primary key (address_id ),
	foreign key (location_id) references locations (location_id)		
);

create table branches (
	branch_id   SERIAL,
	branch_name VARCHAR(350) not null,
	branch_num  INT    not null check (branch_num > 0),
	address_id  INT    not null,
	unique (branch_name, branch_num, address_id),
	primary key (branch_id), 
	foreign key (address_id) references branches_addresses (address_id)
);


--------------------------------------------------------------

-- Passports

create table passports (
	passport_id     SERIAL,
	passport_series INT    not null,
	passport_num    INT    not null,
	issued_by VARCHAR(150) not null,
	issue_date      DATE   not null,
	location_id     INT    not null,
	unique (passport_series, passport_num),
	check  (passport_series > 0  and passport_num > 0),
	primary key (passport_id),
	foreign key (location_id) references locations (location_id)	
);


--------------------------------------------------------------

-- Employees

create table employees (
	employee_id SERIAL,
	name_and_patronymic VARCHAR(150) not null,
	surname VARCHAR(100) not null,
	birthday    DATE     not null,
	passport_id INT      not null unique,
	responsibilities VARCHAR(150) not null,
	branch_id   INT      not null,
	state VARCHAR(50)    not null,
	primary key (employee_id),
	foreign key (passport_id) references passports (passport_id),
	foreign key (branch_id)   references branches  (branch_id) 
);

--------------------------------------------------------------

--Departments

create table departments (
	department_id   SERIAL,
	department_name VARCHAR(350) not null unique,
	primary key (department_id) 
);


create table employee_department (
	emp_dep_id    SERIAL,
	employee_id   INT    not null,
	department_id INT    not null,
	unique (employee_id, department_id),
	primary key (emp_dep_id),
	foreign key (employee_id)   references employees   (employee_id),
	foreign key (department_id) references departments (department_id)
);


--------------------------------------------------------------

-- Contact information

create table phone_numbers (
	phone_num_id SERIAL,
	employee_id  INT         not null,
	phone_num    VARCHAR(12) not null unique,
	primary key (phone_num_id),
	foreign key (employee_id) references employees (employee_id)	
);

create table account_data (
	account_id  SERIAL,
	login       VARCHAR(50) not null,
	"password"  VARCHAR(50) not null,
	employee_id INT         not null unique,
	primary key (account_id),
	foreign key (employee_id) references employees (employee_id) 
);


--------------------------------------------------------------

-- Applications and business trips

create table applications (
	application_id   BIGSERIAL,
	application_type VARCHAR(50) not null,
	status           VARCHAR(10) not null,          /* in process/denied/accepted */
	application_date TIMESTAMP(2) not null,
	solution_date    TIMESTAMP(2),
	date_start       DATE not null,
	date_finish      DATE not null,
	applicant_id     INT  not null,
	solver_id        INT,
	unique (application_type, date_start, date_finish, applicant_id),
	check  ((solver_id is not null and status != 'in process') or (solver_id is null and status = 'in process')),
	primary key (application_id),
	foreign key (applicant_id) references employees (employee_id),
	foreign key (solver_id)    references employees (employee_id)
); 

create table business_trips (
	business_trip_id BIGSERIAL,
	application_id   BIGINT not null unique,
	instruction      text not null,
	employee_id      INT  not null,
	branch_id        INT  not null,
	primary key (business_trip_id),
	foreign key (application_id) references applications (application_id),
	foreign key (employee_id)    references employees    (employee_id),
	foreign key (branch_id)      references branches     (branch_id)
);





