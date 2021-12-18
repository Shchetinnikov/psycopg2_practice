
-- ¬се за€влени€, поданные после 2010 года

select application_date, application_type, applicant_id 
from   applications
where  application_date > date('2010-12-31')
limit  10


-- ќбщее количество сотрудников в зависимости от состо€ни€

select   state, count(*)
from     employees e 
group by state 


-- —ери€ и номер паспортов сотрудников филиала "Flashspan", которые наход€тс€ на служебном месте

with fspan_ids as (
	select branch_id 
	from   branches
	where  branch_name = 'Flashspan'
), emp_passport_ids as (
	select passport_id, employee_id
	from   employees inner join fspan_ids
	on     employees.branch_id = fspan_ids.branch_id and employees.state = 'on duty'
)
select employee_id, passport_series, passport_num
from   passports natural inner join emp_passport_ids


--  оличество человек, наход€щихс€ в отпуске, дл€ каждого подразделени€

with table1 as (
	select *
	from   departments d inner join employee_department ed 
	on     d.department_id = ed.department_id
)
select   department_name, count(state) 
from     table1 t1 inner join employees e 
on       t1.employee_id = e.employee_id
group by t1.department_name, e.state
having   e.state = 'vacation'


-- ¬се филиалы, которые наход€тс€ во ‘ранции.

with fr_regions as (
	select *
	from   countries c inner join regions r 
	on     c.country_name = 'France'and c.country_id = r.country_id 
), fr_locations as (
	select *
	from   fr_regions r inner join locations l 
	on     r.region_id = l.region_id 
), fr_addresses as (
	select *
	from   fr_locations l inner join branches_addresses ba
	on     l.location_id = ba.location_id 
)
select   branch_name, branch_num
from     fr_addresses a inner join branches b 
on       a.address_id = b.address_id 
order by branch_name
limit    10


--  оличество сотрудников подразделени€ Support с одобренными командировками

with engine_id as (
	select department_id 
	from   departments d 
	where  department_name = 'Support'
), engine_emp as (
	select employee_id
	from   employee_department ed inner join engine_id 
	on     ed.department_id = engine_id.department_id
), engine_trips as (
	select application_id
	from   engine_emp inner join business_trips bt 
	on     engine_emp.employee_id = bt.employee_id 
), app_ids as (
	select application_id
	from   applications a 
	where  a.status = 'accepted'
)
select count(*) 
from   engine_trips inner join app_ids
on     engine_trips.application_id = app_ids.application_id
