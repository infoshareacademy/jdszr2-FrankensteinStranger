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

SELECT sum(koszt_zakupu_filmow) AS koszt_zakupu_ALL,
	sum(p.amount) AS przychod_ALL
FROM t1 t1
JOIN inventory i 
	ON t1.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	LEFT JOIN payment p
	ON r.rental_id = p.rental_id
