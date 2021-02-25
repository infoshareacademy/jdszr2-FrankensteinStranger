select 
	max(amount) as max_price,
	min(amount) as min_price ,
	avg(amount) as avg_price,
	percentile_disc(0.25) within group (order by amount) as Q1_price,
	percentile_disc(0.5) within group (order by amount) as Q2_price,
	percentile_disc(0.75) within group (order by amount) as Q3_price,
	percentile_disc(0.95) within group (order by amount) as proc95_price
from payment
where amount > 0 -- 24 rekordy z cen¹ 0

---- sprawdzenie replacement_price czy jest porównywalna z cen¹ filmów w tabeli payment. 
---- Wiêkszoœæ wypo¿yczanych filmów jest wypo¿yczana z mniejsz¹ op³at¹ ni¿ najni¿sza cena replacement_film.
---- Dlatego przyjmujemy, ¿e jedyna informacja o kwocie za wynajem to zmienna amount z tabeli payment
 
select 
	max(replacement_cost) as max_price,
	min(replacement_cost) as min_price ,
	avg(replacement_cost) as avg_price
from film f 

--------
-- tabela payment z dodan¹ kategoryzacj¹ ceny filmów 
-------- Najpierw sprawdzê jaka jest œrednia iloœæ wypo¿yczeñ pojedyñczego filmu. 
-------- Oznacze binarnie czy film wypo¿ycza³ siê czêœciej ni¿ œrednia 1 - TAK, 0 - NIE
-------- Policzê information Value dla zmiennej objaœnianaej, któr¹ stworzy³em po zmiennych objaœniaj¹cych w tym cena

create or replace view film1 as
with rental_filmid as (
select 
	r.*, 
	i.film_id 
from rental r
	left join inventory i on r.inventory_id =i.inventory_id 
	--left join film f on f.film_id =i.film_id 
),

film_id_count as (
select 
	film_id,
	count(film_id) as ilosc
from rental_filmid
group by 1
)

--select percentile_disc(0.75) within group (order by ilosc) as Q2_ilosc
--from film_id_count

-- mediana iloœci wypo¿yczeñ dla pojedyñczego filmu wynosi 16

-- poni¿ej tabela film z dodan¹c oznczeniem czy sprzedaz tytu³u by³a wiêksza ni¿ mediana

select *,
case 
	when film_id in (select film_id	
					 from film_id_count
					 where ilosc > 22 ) then 1 else 0 end  as wieksze_od_median,
case 
	when replacement_cost <= (select percentile_disc(0.25) within group (order by replacement_cost) as Q1_price from film f2) then 1
	when replacement_cost <= (select percentile_disc(0.50) within group (order by replacement_cost) as Q2_price from film f2) then 2
	when replacement_cost <= (select percentile_disc(0.75) within group (order by replacement_cost) as Q3_price from film f2) then 3
	else 4 end as kategoria_cenowa
from film f
;

----- do tabeli dodaje tabele kategorie oraz liczbê wypo¿yczeñ 
create or replace view film2 as
with rental_filmid as (
select 
	r.*, 
	i.film_id 
from rental r
	left join inventory i on r.inventory_id =i.inventory_id 
	--left join film f on f.film_id =i.film_id 
),

film_id_count as (
select 
	film_id,
	count(film_id) as ilosc
from rental_filmid
group by 1
)


select 
film1.*, c.name as kategoria, fic.ilosc
from film1 
left join film_category fc using(film_id)
left join category c using(category_id)
left join film_id_count fic using(film_id)
;

-----liczymy information value na widoku film1
select * from film1
-----

with tabela1 as (select kategoria,
count(case when wieksze_od_median = 1 then wieksze_od_median end) as GOOD,
count(case when wieksze_od_median = 0 then wieksze_od_median end) as BAD,
(count(case when wieksze_od_median = 1 then wieksze_od_median end))/(select count(*) from film1 ao2 where wieksze_od_median = 1)::numeric as DG,
(count(case when wieksze_od_median = 0 then wieksze_od_median end))/(select count(*) from film1 ao2 where wieksze_od_median = 0)::numeric as DB

from film2
group by 1
order by 2 desc),

table2 as (
select *,
ln(dg/db) as WOE,
dg - db as "DG - DB"

from tabela1

),

tabela3 as(
select *, ("DG - DB" * WOE) as "(DG-DB)*WOE"  from table2)

--select * from tabela3

select sum("(DG-DB)*WOE") from tabela3


--- korelacja 
-- korelacja zmiennych liczbowych ci¹g³ych ze zmienn¹ ilosc(liczba wypozyczen filmu)
select 
	corr(kategoria_cenowa, ilosc) as corr_kategoria_cenowa,
	corr(rental_duration, ilosc) as corr_rental_duration,
	corr(rental_rate, ilosc) as corr_rental_rate,
	corr(length, ilosc) as corr_length,
	corr(replacement_cost, ilosc) as corr_replacement_cost,
	corr(length(description), ilosc) as corr_dlugosc_opisu
from film2




