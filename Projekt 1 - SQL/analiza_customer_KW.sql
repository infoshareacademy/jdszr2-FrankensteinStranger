
-- ilość klientów, którzy zwracają filmy do 3 dni po terminie, więcej niż trzy dni po terminie i niezwrocone

WITH t1 AS 
( 
SELECT r.rental_id, r.customer_id, return_date,
	(f.rental_duration - date_part('day', return_date-rental_date))::integer AS date_diff
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	INNER JOIN payment p
	ON r.rental_id = p.rental_id  
)
SELECT count(DISTINCT(customer_id)) AS cnt_customer,
	count (DISTINCT(CASE WHEN date_diff <= 3 THEN customer_id end )) AS trzy_dni_i_mniej,
	count (DISTINCT(CASE WHEN date_diff > 3 THEN customer_id end )) AS wiecej_niz_3_dni,
	count (DISTINCT(CASE when return_date IS NULL THEN customer_id end)) AS niezwrocone
FROM t1

-- procent filmów zwracanych po terminie lub niezwracanych wcale przez klientów

WITH t1 AS
(
SELECT r.customer_id, r.rental_id, f.film_id, i.inventory_id, f.rental_rate, p.amount,
	CASE WHEN p.amount - f.rental_rate > 0 THEN 'nadplata' 
		 WHEN p.amount - f.rental_rate = 0 THEN 'oplacony 'ELSE 'nieoplacony' END AS status_platnosci, 
	CASE WHEN return_date IS NOT NULL AND f.rental_duration < date_part('day', return_date-rental_date) THEN 'opozniony' 
		WHEN return_date IS NULL THEN 'niezwrocony'
	ELSE 'na_czas' end AS status_zwrotu
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	INNER JOIN payment p
	ON r.rental_id = p.rental_id 
ORDER BY f.film_id 
), 
t2 AS 
(
SELECT customer_id, 
	count(rental_id) AS cnt_rent,
	count(CASE WHEN status_zwrotu = 'opozniony' THEN rental_id END) AS cnt_opoznione,
	count(CASE WHEN status_zwrotu = 'niezwrocony' THEN rental_id END) AS cnt_niezwrocony
FROM t1
GROUP BY customer_id
)

SELECT 
	round(cnt_opoznione/cnt_rent::NUMERIC,2) AS proc_opoznione,
	--round(cnt_niezwrocony/cnt_rent::NUMERIC,2) AS proc_niezwrocony,
	count(customer_id) AS ilosc_klientow 
FROM t2
GROUP BY round(cnt_opoznione/cnt_rent::NUMERIC,2)
--round(cnt_niezwrocony/cnt_rent::NUMERIC,2)
ORDER BY 1 desc
