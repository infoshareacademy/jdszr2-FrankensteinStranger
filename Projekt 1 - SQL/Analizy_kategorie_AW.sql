-- widok klient -> miasto -> państwo

create view customer_city_country as
	select
		customer_id,
		c2.city,
		c3.country
	from customer c
		join address a on c.address_id = a.address_id
		join city c2 on a.city_id = c2.city_id
		join country c3 on c2.country_id = c3.country_id

-- adresy sklepów

select
	*
from store s
	join address a on s.address_id = a.address_id
	join city c on a.city_id = c.city_id
	join country c2 on c.country_id = c2.country_id 

-- liczba filmów w danej kategorii
select 
	distinct c.name, 
	count(*) 
from film f
	join film_category fc on f.film_id = fc.film_id 
	join category c on fc.category_id = c.category_id 
		group by c.name
		order by 2 DESC

-- liczba kopii w danej kategorii

select  
	c.name, 
	count(*)
from film f
	join film_category fc on f.film_id = fc.film_id 
	join category c on fc.category_id = c.category_id 
	join inventory i on f.film_id = i.film_id 
	join store s on i.store_id = s.store_id 
		group by 1
		order by 1,2 desc 	

-- liczba tytułów i kopii w podziale na kategorie

with aaa as 
(select  
	c.name as kategoria, 
	count(*) as l_kopii
from film f
	join film_category fc on f.film_id = fc.film_id 
	join category c on fc.category_id = c.category_id 
	join inventory i on f.film_id = i.film_id 
	join store s on i.store_id = s.store_id 
		group by 1
		order by 1,2 desc),
bbb as		
(select 
	distinct c.name kategoria, 
	count(*) as l_filmow
from film f
	join film_category fc on f.film_id = fc.film_id 
	join category c on fc.category_id = c.category_id 
		group by c.name
		order by 2 desc),
ccc as 
(select a.kategoria, l_kopii, l_filmow from aaa a  join bbb b on a.kategoria = b.kategoria)
select * from ccc
		

-- liczba kopii w danej kategorii z podziałem na wypozyczalnię 

select 
	s.store_id, 
	c.name, 
	count(*)
from film f
	join film_category fc on f.film_id = fc.film_id 
	join category c on fc.category_id = c.category_id 
	join inventory i on f.film_id = i.film_id 
	join store s on i.store_id = s.store_id 
		group by 1,2
		order by 1,3 desc 	

-- liczba wypoyczeń w podziale na kategorie

select 
	c.name as kategoria,
	count(rental_id) as liczba_wypozyczen
from rental r 
	join inventory i on r.inventory_id = i.inventory_id 
	join film f on i.film_id =f.film_id 
	join film_category fc on f.film_id = fc.film_id 
	join category c on fc.category_id = c.category_id 
		group by 1
		order by 2 desc		

-- adresy wypozyczalni

select 
	s.store_id, 
	c2.country,
	c.city,
	a.address 
from store s 
	join address a ON s.address_id = a.address_id 
	join city c on a.city_id = c.city_id 
	join country c2 on c.country_id = c2.country_id 

-- przychody z danej kategorii

select 
	c.name as kategoria, 
	sum(p.amount) as przychód 
from rental r 
	join inventory i on r.inventory_id = i.inventory_id 
	join film f on i.film_id = f.film_id 
	join film_category fc  on f.film_id = fc.film_id
	join category c on fc.category_id = c.category_id 
	left join payment p on r.rental_id = p.rental_id 
		group by 1
		order by 2 desc

-- przychody + liczba wypozyczen z podzialem na kategorie		

-- cennik filmów + lista wypozyczen

select 
	distinct amount as cena,
	count(rental_id) as liczba_wypozyczen
from payment p 
	group by 1
	order by 2 desc

-- 	sprawdzenie max, min, avg, percentyli liczby wypozyczeń danego tytułu filmu

with aaa as 
	(select 
		film_id, 
		count(*) as lw 
	from rental r 
		join inventory i on r.inventory_id = i.inventory_id 
			group by 1
			order by 2 desc),
bbb as 
	(select 
		distinct lw 
	from aaa)
select 
	max(lw), 
	min(lw), 
	avg(lw),
	percentile_disc(0.5) within group (order by lw) as mediana,
	percentile_disc(0.25) within group (order by lw) as Q1,
	percentile_disc(0.75) within group (order by lw) as Q3
from bbb 

-- max, min, avg, sum, odchylenie i wariancja przychodów w podziale na kategorie
-- z wykluczeniem wypozyczen, gdzie payment = 0 

select 
	c.name as kategoria, 
	sum(p.amount) as przychód,
	avg(p.amount) as avg_przychód,
	max(p.amount) as max_przychod,
	min(p.amount) as min_przychód,
	stddev(p.amount) as odchylenie_przychód,
	variance(p.amount) as wariancja_przychód 
from rental r 
	join inventory i on r.inventory_id = i.inventory_id 
	join film f on i.film_id = f.film_id 
	join film_category fc  on f.film_id = fc.film_id
	join category c on fc.category_id = c.category_id 
	left join payment p on r.rental_id = p.rental_id 
	where p.amount > 0
		group by 1
		order by 2 desc

-- przychody z danego tytułu + liczba wypozyczeń

select 
	f.film_id,
	f.title, 
	sum(p.amount),
	count(r.rental_id)
from rental r 
	join inventory i on r.inventory_id = i.inventory_id 
	join film f on i.film_id = f.film_id 
	join film_category fc  on f.film_id = fc.film_id
	join category c on fc.category_id = c.category_id 
	left join payment p on r.rental_id = p.rental_id 
	where p.amount > 0
		group by 1
		order by 3 desc

-- korelacja między kategorią a ceną - BRAK - 6%

select 
	corr(c.category_id, p.amount)
from rental r 
	join inventory i on r.inventory_id = i.inventory_id 
	join film f on i.film_id = f.film_id 
	join film_category fc  on f.film_id = fc.film_id
	join category c on fc.category_id = c.category_id 
	left join payment p on r.rental_id = p.rental_id 
	where p.amount > 0

-- ilość wypozyczen w danym kraju

select 
	c3.country, 
	count(r.rental_id) 
from rental r 
	join customer c on r.customer_id = c.customer_id 
	join address a on c.address_id = a.address_id 
	join city c2 on a.city_id = c2.city_id 
	join country c3 on c2.country_id = c3.country_id 
		group by 1
		order by 2 desc

-- najpopularniejszy aktor pod względem przychodów z tytułów i liczby wypozyczen

select 
	a.actor_id, 
	a.first_name, 
	a.last_name, 
	count(r.rental_id), 
	sum(p.amount) 
from actor a 
	join film_actor fa on a.actor_id = fa.actor_id 
	join film f on fa.film_id = f.film_id 
	join inventory i on f.film_id = i.film_id 
	join rental r on i.inventory_id = r.inventory_id
	join payment p on r.rental_id = p.rental_id 
		group by 1,2,3
		order by 5 desc 

-- aktor, liczba filmów w których zagrał, przychód na danego aktora


with aaa as
(select 
	a.actor_id, 
	a.first_name as imie,
	a.last_name as nazwisko,
	sum(p.amount) as przychód
from actor a 
	join film_actor fa on a.actor_id = fa.actor_id 
	join film f on fa.film_id = f.film_id 
	join inventory i on f.film_id = i.film_id 
	join rental r on i.inventory_id = r.inventory_id
	join payment p on r.rental_id = p.rental_id
		group by 1,2,3
		),
bbb as 
(SELECT actor_id, count(*) Ile_filmow
FROM actor AS a
JOIN film_actor AS fa USING (actor_id)
GROUP BY 1
ORDER BY Ile_filmow desc),
ccc as
(select 
	a.imie as imie, 
	a.nazwisko as nazwisko, 
	b.Ile_filmow as lp_film, 
	a.przychód as przych
from aaa a 
	join bbb b on a.actor_id = b.actor_id 
		group by 1, 2, 3, 4 
		order by ile_filmow desc)
select 
	imie, 
	nazwisko, 
	lp_film, 
	przych,
	(select stddev(przych) from ccc) as odchylenie, -- na przychodach wszystkich aktorów
	(select variance(przych) from ccc) as wariancja -- na przychodach wszystkich aktorów
from ccc 
	group by 1,2,3,4
	order by 3 desc 

-- rating -> przychód, liczba kopii, liczba tytułów, liczba wypozyczen

with aaa as
(select 
	f.rating as rating, 
	sum(p.amount) as przychód,
	count(r.rental_id) as l_wypoz
from rental r 
	join inventory i on r.inventory_id = i.inventory_id 
	join film f on i.film_id = f.film_id 
	join film_category fc  on f.film_id = fc.film_id
	join category c on fc.category_id = c.category_id 
	left join payment p on r.rental_id = p.rental_id 
		group by 1),
bbb as		
(select 
	f2.rating as rating, 
	count(i2.inventory_id) as liczba_kopii 
from film f2 
	join inventory i2 on f2.film_id = i2.film_id
		group by 1),	
ccc as 		
(select 
	f2.rating as rating, 
	count(f2.film_id) as liczba_tyt
from film f2 
		group by 1)		
select 
	aaa.rating, 
	aaa.przychód, 
	aaa.l_wypoz, 
	bbb.liczba_kopii, 
	ccc.liczba_tyt 
from ccc 
	join bbb on ccc.rating = bbb.rating 
	join aaa on bbb.rating = aaa.rating	