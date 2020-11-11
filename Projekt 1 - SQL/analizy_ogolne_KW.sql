-- podliczenie zakupu wszystkich filmów (ilość kopii * replacement_cost) i podliczenie wszystkich wpływów pieniężnych
-- Wypożyczalnia jest w tragicznej sytuacji finansowej

WITH t1 AS 
( 
SELECT f.film_id, 
	count(DISTINCT(i.inventory_id)) AS cnt_kopii,
	f.replacement_cost, 
	count(DISTINCT(i.inventory_id)) * replacement_cost AS koszt_zakupu_filmow
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	LEFT JOIN payment p
	ON r.rental_id = p.rental_id 
GROUP BY f.film_id
ORDER BY f.film_id
)

SELECT sum(koszt_zakupu_filmow) AS koszt_zakupu_ALL
FROM t1 -- koszt zakupu filmów

SELECT sum(amount) FROM payment -- wszystkie wpływy pieniężne

-- analiza ogólna wypożyczeń:
-- 1. wypożyczenia opłacone, nieopłacone i nadpłacone
-- 2. wypożyczenia oddane na czas, opóźnione i niezwrócone

WITH t1 AS
(
SELECT r.customer_id, r.rental_id, f.film_id, i.inventory_id, f.rental_rate, p.amount,
	CASE WHEN p.amount - f.rental_rate > 0 THEN 'nadplata' 
		 WHEN p.amount - f.rental_rate = 0 THEN 'oplacony' ELSE 'nieoplacony' END AS status_platnosci, 
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
SELECT 
	count(rental_id) AS cnt_rent,
	count(CASE WHEN status_platnosci in ('oplacony', 'nadplata') THEN rental_id END) AS cnt_oplacony,
	count(CASE WHEN status_platnosci = 'nieoplacony' THEN rental_id END) AS cnt_nieoplacone,
	count(CASE WHEN status_platnosci = 'nadplata' THEN rental_id END) AS cnt_nadplata,
	count(CASE WHEN status_zwrotu = 'na_czas' THEN rental_id END) AS cnt_na_czas,
	count(CASE WHEN status_zwrotu = 'opozniony' THEN rental_id END) AS cnt_opoznione,
	count(CASE WHEN status_zwrotu = 'niezwrocony' THEN rental_id END) AS cnt_niezwrocony
FROM t1
