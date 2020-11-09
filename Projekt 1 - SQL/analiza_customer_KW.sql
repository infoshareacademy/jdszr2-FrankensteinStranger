
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

-- ilość klientów, w których koszyku:
-- 1. ponad 50% filmów jest zwróconych z opóźnieniem
-- 2. między 50% a 10% filmów jest zwróconych z opóźnieniem
-- 3. mniej niż 10% filmów jest zwróconych z opóźnieniem
-- 4. ilość klientów, którzy choć raz nie zwrócili filmu
-- 5. ilośc klientów, dla którzy nie zwracają 5% lub więcej swoich zamówień (ale mniej niż 10%)

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
	count(DISTINCT(rental_id)) AS rent_cnt,
	count(CASE WHEN status_zwrotu = 'opozniony' THEN rental_id END) AS ilosc_opoznionych,
	count(CASE WHEN status_zwrotu = 'niezwrocony' THEN rental_id END ) AS ilosc_niezwroconych
FROM t1
GROUP BY customer_id
ORDER BY 3 desc
),
t3 AS 
( 
SELECT customer_id,
	(ilosc_opoznionych::numeric/rent_cnt) AS wsp_opoznionych,
	(ilosc_niezwroconych::numeric/rent_cnt) AS wsp_niezwroconych
FROM t2
ORDER BY 2 DESC
)

SELECT count(DISTINCT(customer_id)) AS cnt_customer,
	count(CASE WHEN wsp_opoznionych > 0.5 THEN customer_id END) AS ponad_50proc_opoznionych,
	count(CASE WHEN wsp_opoznionych < 0.5 AND wsp_opoznionych > 0.1 THEN customer_id END) AS miedzy_50_i_10_proc,
	count(CASE WHEN wsp_opoznionych < 0.1 THEN customer_id END) AS mniej_niz_10_proc,
	count(CASE WHEN wsp_niezwroconych > 0 THEN customer_id END) AS niezwrone,
	count(CASE WHEN wsp_niezwroconych >= 0.05 THEN customer_id END) AS wiecej_niz_5_proc_niezwroconych
FROM t3
