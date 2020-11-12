
-- ile wypozycza 
-- jak poszczegolne segmenty wypozyczaj¹ w poszczególnych kategoriach 

-- rozk³ad iloœci klientów wzglêdem liczby wypo¿yczeñ 
with cutomers_rental_count as (
select 
	customer_id, 
	count(*) as rentals_count from rental 
group by 1 
order by 2 desc)

select 
	rentals_count, 
	count(*) as customers
from cutomers_rental_count
group by 1
order by 2 desc

-- Podzia³ klientów  na 4 równe segmenty wzglêdem iloœci wypo¿yczeñ 
with cutomers_rental_count as (
select 
	customer_id, 
	count(*) as rentals_count from rental 
group by 1 ), 

customers_rental_count_all as (select *
from customer c left join cutomers_rental_count using(customer_id))

select 
	max(rentals_count) as max_ilosc_wypozyczen,
	min(rentals_count) as min_ilosc_wypozyczen ,
	avg(rentals_count) as avg_ilosc_wypozyczen,
	percentile_disc(0.25) within group (order by rentals_count) as Q1_ilosc_wypozyczen,
	percentile_disc(0.5) within group (order by rentals_count) as Q2_ilosc_wypozyczen,
	percentile_disc(0.75) within group (order by rentals_count) as Q3_ilosc_wypozyczen,
	percentile_disc(0.95) within group (order by rentals_count) as proc95_ilosc_wypozyczen
from customers_rental_count_all

---Kateogryzacja klientów wzglêdem ilosci wypoczyceñ 1,2,3,4

with cutomers_rental_count as (
select 
	customer_id, 
	count(*) as rentals_count from rental 
group by 1 ), 

customers_rental_count_all as (select *
from customer c left join cutomers_rental_count using(customer_id))

select *,
case 
	when rentals_count <= (select percentile_disc(0.25) within group (order by rentals_count)  from cutomers_rental_count f2) then 1
	when rentals_count <= (select percentile_disc(0.50) within group (order by rentals_count)  from cutomers_rental_count f2) then 2
	when rentals_count <= (select percentile_disc(0.75) within group (order by rentals_count)  from cutomers_rental_count f2) then 3
	else 4 end as kat_ilosc_wypo


from customers_rental_count_all

----- 
-----
--Doci¹gamy kateogoriê filmów do segmentów, 

with cutomers_rental_count as (
select 
	customer_id, 
	count(*) as rentals_count 
from rental 
group by 1 ), 

customers_rental_count_all as (
select 
	*
from customer c 
left join cutomers_rental_count using(customer_id)),

customers_kat as (
select *,
case 
	when rentals_count <= (select percentile_disc(0.25) within group (order by rentals_count)  from cutomers_rental_count f2) then 1
	when rentals_count <= (select percentile_disc(0.50) within group (order by rentals_count)  from cutomers_rental_count f2) then 2
	when rentals_count <= (select percentile_disc(0.75) within group (order by rentals_count)  from cutomers_rental_count f2) then 3
	else 4 end as kat_ilosc_wypo
from customers_rental_count_all), 

customers_3 as (
select 
	r.*,
	crc.rentals_count,
	crc.kat_ilosc_wypo,
	c.name as kategoria
from rental r 
	left join customers_kat crc using(customer_id) 
	left join inventory using(inventory_id)
	left join film f2 using(film_id)
	left join film_category fc using(film_id)
	left join category c using(category_id))
	
select kat_ilosc_wypo, kategoria, count(*)
from customers_3
group by 1,2
order by 1,3 desc


