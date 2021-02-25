
-- ilość klientów, którzy zwracają filmy do 3 dni po terminie, więcej niż trzy dni po terminie i niezwrocone
-- każdy klient, chociaż raz zwrocił film z opóźnieniem

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
	count (DISTINCT(CASE WHEN date_diff >= -3 AND date_diff < 0 then customer_id end )) AS trzy_dni_i_mniej,
	count (DISTINCT(CASE WHEN date_diff < -3 THEN customer_id end )) AS wiecej_niz_3_dni,
	count (DISTINCT(CASE when return_date IS NULL THEN customer_id end)) AS niezwrocone
FROM t1

-- procentowy rozkład filmów zwracanych z opóźnieniem do 3 dni i ponad 3 dni per klient (brane pod uwagę jako 100% tylko filmy oddane po terminie).

WITH t1 AS
(
SELECT r.customer_id, r.rental_id, f.film_id, i.inventory_id, f.rental_rate, 
	(f.rental_duration - date_part('day', return_date-rental_date))::integer AS date_diff,
	CASE WHEN return_date IS NOT NULL AND f.rental_duration < date_part('day', return_date-rental_date) THEN 'opozniony' 
		WHEN return_date IS NULL THEN 'niezwrocony'
	ELSE 'na_czas' end AS status_zwrotu
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
ORDER BY i.inventory_id 
), 
t2 AS 
(
SELECT customer_id, 
	count(rental_id) AS cnt_rent,
	count(CASE WHEN date_diff >= -3 THEN rental_id END) AS cnt_opoznione_do_3_dni,
	count(CASE WHEN date_diff < -3 THEN rental_id END) AS cnt_opoznione_ponad_3_dni
FROM t1
WHERE status_zwrotu = 'opozniony'
GROUP BY customer_id
)
SELECT 
	round(cnt_opoznione_do_3_dni/cnt_rent::NUMERIC,2) AS proc_opoznione_do_3_dni,
	round(cnt_opoznione_ponad_3_dni/cnt_rent::NUMERIC,2) AS proc_opoznione_ponad_3_dni,
	customer_id
FROM t2
ORDER BY customer_id

-- ilość filmów oddanych po terminie per ilość dni 

WITH t1 AS
(
SELECT r.customer_id, r.rental_id, f.film_id, i.inventory_id, f.rental_rate, 
	(f.rental_duration - date_part('day', return_date-rental_date))::integer AS date_diff,
	CASE WHEN return_date IS NOT NULL AND f.rental_duration < date_part('day', return_date-rental_date) THEN 'opozniony' 
		WHEN return_date IS NULL THEN 'niezwrocony'
	ELSE 'na_czas' end AS status_zwrotu
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	LEFT JOIN payment p
	ON r.rental_id = p.rental_id 
ORDER BY i.inventory_id 
)
SELECT count(rental_id),
	abs(date_diff) AS dni_opoznienia
FROM t1
WHERE status_zwrotu = 'opozniony'
GROUP BY date_diff 
ORDER BY date_diff


-- procent filmów zwracanych po terminie lub niezwracanych wcale przez klientów

WITH t1 AS
(
SELECT r.customer_id, r.rental_id, f.film_id, i.inventory_id, f.rental_rate, 
	CASE WHEN return_date IS NOT NULL AND f.rental_duration < date_part('day', return_date-rental_date) THEN 'opozniony' 
		WHEN return_date IS NULL THEN 'niezwrocony'
	ELSE 'na_czas' end AS status_zwrotu
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	JOIN rental r
	ON i.inventory_id = r.inventory_id
ORDER BY i.inventory_id 
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

-- wykomentowane linie należy zamienić, żeby zpbaczyć procent niezwróconych filmów 
SELECT 
	round(cnt_opoznione/cnt_rent::NUMERIC,2) AS proc_opoznione,
	--round(cnt_niezwrocony/cnt_rent::NUMERIC,2) AS proc_niezwrocony,
	count(customer_id) AS ilosc_klientow 
FROM t2
GROUP BY round(cnt_opoznione/cnt_rent::NUMERIC,2)
--round(cnt_niezwrocony/cnt_rent::NUMERIC,2)
ORDER BY 1 desc
