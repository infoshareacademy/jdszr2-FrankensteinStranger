---- Potrzebne tabele

select * from actor a 
select * from film_actor fa --- ³¹czy sie z actor po actor_id
select * from film f  --- ³¹czy sie z film_actor po film_id
select * from inventory i  --- ³¹czy sie z film po film_id
select * from rental r --- ³¹czy sie z inventory po inventory_id
select * from payment p --- ³¹czy sie z rental po rental_id


--- ile wydane na wypo¿yczenia
select sum(amount) from payment p 



--- Sprawdzenie w ilu filmach gra³ dany aktor


SELECT first_name, last_name, count(*) Ile_filmow
FROM actor AS a
JOIN film_actor AS fa USING (actor_id)
GROUP BY actor_id, first_name, last_name
ORDER BY Ile_filmow desc;

SELECT first_name, last_name, count(*) filmy
FROM actor AS a
JOIN film_actor AS fa USING (actor_id)
GROUP BY actor_id, first_name, last_name
ORDER BY filmy DESC
LIMIT 10;


---------------------		

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
		order by Ile_filmow desc)
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
------------------


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
	b.Ile_filmow as liczba_filmów, 
	a.przychód as przych
from aaa a
	join bbb b on a.actor_id = b.actor_id 
		group by 1, 2, 3, 4 
		order by Ile_filmow desc)
select 
	imie, 
	nazwisko, 
	liczba_filmów, 
	przych,
	round( przych / liczba_filmów,1) as avg_aktor_film, --- zarobek z filmu per aktor
	(select round( avg(przych), 1) from ccc) as œrednia, -- œredni przychód z wypo¿yczeñ na jednego aktora
	(select round(stddev(przych),1) from ccc) as odchylenie, -- na przychodach wszystkich aktorów
	(select round(variance(przych),1) from ccc) as wariancja -- na przychodach wszystkich aktorów
	
from ccc 
	group by 1,2,3,4
	order by avg_aktor_film  desc
	limit 10 ;