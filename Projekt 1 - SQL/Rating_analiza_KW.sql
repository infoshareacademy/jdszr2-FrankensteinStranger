--CEL: sprawdzenie czy rating filmu ma wpływ na jego popularność, przychód

-- sprawdzenie ile filmów wypada na dany rating, ile mamy kopii takich filmów (jeden film możemy mieć w więcej niż jednej sztuce) i ile wypożyczeń

SELECT rating, 
	count(DISTINCT(f.film_id)) AS cnt_films,
	count(DISTINCT(i.inventory_id )) AS cnt_copy_no,
	count(DISTINCT(r.rental_id)) AS rent_cnt, 
	sum(p.amount) AS przychod,
	sum(p.amount)/count(DISTINCT(i.inventory_id )) AS AVG_przychód_per_kopia,
	sum(p.amount)/count(DISTINCT(r.rental_id)) AS AVG_przychód_per_rent
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	INNER JOIN payment p
	ON r.rental_id = p.rental_id 
GROUP BY rating 
ORDER BY rating; 

-- dodatkowo z podziałem na sklepy (rozkład jest podobny w obu)

SELECT rating, i.store_id, 
	count(DISTINCT(f.film_id)) AS cnt_films,
	count(DISTINCT(i.inventory_id )) AS cnt_copy_no,
	count(DISTINCT(r.rental_id)) AS rent_cnt, 
	sum(p.amount) AS przychod
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	INNER JOIN payment p
	ON r.rental_id = p.rental_id 
GROUP BY rating, i.store_id 
ORDER BY i.store_id, rating; 

-- mediana ceny wypożyczenia i kwartyle dla każdego ratingu (+ wersja z rozróżnieniem na sklepy)

SELECT rating,
	percentile_disc(0.5) WITHIN GROUP (ORDER BY p.amount) AS MEDIANA_cena,
	percentile_disc(array[0.25, 0.5, 0.75]) WITHIN GROUP (ORDER BY p.amount) AS kwartyle_cena
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	INNER JOIN payment p
	ON r.rental_id = p.rental_id 
GROUP BY rating
ORDER BY rating;
--
SELECT rating, i.store_id, 
	percentile_disc(0.5) WITHIN GROUP (ORDER BY p.amount) AS MEDIANA_cena,
	percentile_disc(array[0.25, 0.5, 0.75]) WITHIN GROUP (ORDER BY p.amount) AS kwartyle_cena
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	INNER JOIN payment p
	ON r.rental_id = p.rental_id 
GROUP BY rating, i.store_id 
ORDER BY i.store_id, rating ;

-- średnia, odchylenie i wariancja - nic ciekawego (+ wresja z rozróżnieniem na sklepy)

SELECT rating,
	avg(p.amount) AS srednia,
	stddev(p.amount) AS odchylenie,
	variance(p.amount) AS wariancja,
	count(r.rental_id) AS ilosc_wypozyczen
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	INNER JOIN payment p
	ON r.rental_id = p.rental_id 
GROUP BY rating
ORDER BY rating;
--
SELECT rating, i.store_id, 
	avg(p.amount) AS srednia,
	stddev(p.amount) AS odchylenie,
	variance(p.amount) AS wariancja,
	count(r.rental_id) AS ilosc_wypozyczen
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	INNER JOIN payment p
	ON r.rental_id = p.rental_id 
GROUP BY rating, store_id
ORDER BY i.store_id, rating;

--współczynnik filmów niezwróconych (+ per sklep, też nic ciekawego)

SELECT rating, 
	count(DISTINCT(r.rental_id)) AS cnt_wypozyczen,
	count(CASE WHEN r.return_date IS NULL THEN r.rental_id END) AS niezwrocone,
	count(CASE WHEN r.return_date IS NULL THEN r.rental_id END)::numeric / count(r.rental_id) AS wsp_niezwroconych
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	INNER JOIN payment p
	ON r.rental_id = p.rental_id
GROUP BY rating
ORDER BY rating; 
--
SELECT rating, i.store_id, 
	count(DISTINCT(r.rental_id)) AS cnt_wypozyczen,
	count(CASE WHEN r.return_date IS NULL THEN r.rental_id END) AS niezwrocone,
	count(CASE WHEN r.return_date IS NULL THEN r.rental_id END)::numeric / count(r.rental_id) AS wsp_niezwroconych
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	INNER JOIN payment p
	ON r.rental_id = p.rental_id
GROUP BY rating, i.store_id 
ORDER BY i.store_id, rating; 

-- średnia długość wypożyczenia podobna dla wszystkich kategorii

SELECT rating, 
	avg(CASE WHEN r.return_date IS NOT NULL 
	THEN date_part('day', r.return_date - r.rental_date) END) AS avg_dlugosc_wyp
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	INNER JOIN payment p
	ON r.rental_id = p.rental_id
GROUP BY rating
ORDER BY rating; 

-- ilość nieopłaconych wypożyczeń + współczynnik nieopłaconych wypożyczeń per kategoria (+sklep w drugiej wersji)

SELECT rating,
	count(DISTINCT(r.rental_id)) AS rent_cnt,
	count(CASE WHEN p.payment_id IS NULL THEN r.rental_id end) ilosc_nieoplaconych,
	count(CASE WHEN p.payment_id IS NULL THEN r.rental_id END)::numeric / count(r.rental_id) AS wsp_nieoplaconych
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	LEFT JOIN payment p
	ON r.rental_id = p.rental_id
GROUP BY rating
ORDER BY rating; 
--
SELECT rating, i.store_id, 
	count(DISTINCT(r.rental_id)) AS rent_cnt,
	count(CASE WHEN p.payment_id IS NULL THEN r.rental_id end) ilosc_nieoplaconych,
	count(CASE WHEN p.payment_id IS NULL THEN r.rental_id END)::numeric / count(r.rental_id) AS wsp_nieoplaconych
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	LEFT JOIN payment p
	ON r.rental_id = p.rental_id
GROUP BY rating, i.store_id 
ORDER BY i.store_id, rating; 

--ilość i współczynnik filmów zwracanych przed terminem, na czas i z opóźnieniem (+ podział na sklepy)

WITH t1 AS 
(
SELECT *, 
	date_part('day', return_date-rental_date) AS date_diff
FROM rental)

SELECT f.rating,
	count(DISTINCT(r.rental_id)) AS rent_cnt, 
	count(CASE WHEN f.rental_duration > t1.date_diff THEN r.rental_id END) AS cnt_returned_early,
	count(CASE WHEN f.rental_duration = t1.date_diff THEN r.rental_id END) AS cnt_returned_on_time,
	count(CASE WHEN f.rental_duration < t1.date_diff THEN r.rental_id END) AS cnt_return_late,
	count(CASE WHEN f.rental_duration > t1.date_diff THEN r.rental_id END)::numeric / count(r.rental_id) AS wsp_returned_early,
	count(CASE WHEN f.rental_duration = t1.date_diff THEN r.rental_id END)::numeric / count(r.rental_id) AS wsp_returned_on_time,
	count(CASE WHEN f.rental_duration < t1.date_diff THEN r.rental_id END)::numeric / count(r.rental_id) AS wsp_return_late
FROM film f
	JOIN inventory i 
		ON f.film_id = i.film_id
	JOIN rental r
		ON i.inventory_id = r.inventory_id
	JOIN t1
		ON t1.rental_id = r.rental_id 
GROUP BY f.rating
ORDER BY f.rating;

WITH t1 AS 
(
SELECT *, 
	date_part('day', return_date-rental_date) AS date_diff
FROM rental)
--
SELECT f.rating, i.store_id, 
	count(DISTINCT(r.rental_id)) AS rent_cnt, 
	count(CASE WHEN f.rental_duration > t1.date_diff THEN r.rental_id END) AS cnt_returned_early,
	count(CASE WHEN f.rental_duration = t1.date_diff THEN r.rental_id END) AS cnt_returned_on_time,
	count(CASE WHEN f.rental_duration < t1.date_diff THEN r.rental_id END) AS cnt_return_late,
	count(CASE WHEN f.rental_duration > t1.date_diff THEN r.rental_id END)::numeric / count(r.rental_id) AS wsp_returned_early,
	count(CASE WHEN f.rental_duration = t1.date_diff THEN r.rental_id END)::numeric / count(r.rental_id) AS wsp_returned_on_time,
	count(CASE WHEN f.rental_duration < t1.date_diff THEN r.rental_id END)::numeric / count(r.rental_id) AS wsp_return_late
FROM film f
	JOIN inventory i 
		ON f.film_id = i.film_id
	JOIN rental r
		ON i.inventory_id = r.inventory_id
	JOIN t1
		ON t1.rental_id = r.rental_id 
GROUP BY f.rating, i.store_id 
ORDER BY i.store_id, f.rating;

-- Czy rating ma wpływ na to czy zakup filmu się zwraca? Information value < 0.02, słaba predykcja, nie nadaje się.
-- ALE: dużo filmów się nie zwróciło 

SELECT rating, 
	avg(replacement_cost/rental_rate) AS po_ilu_zwrot
FROM film
GROUP BY rating;

WITH t1 AS
(
SELECT f.rating, i.inventory_id, f.replacement_cost/f.rental_rate AS return_rate
FROM inventory i
JOIN film f
ON f.film_id = i.film_id 
),
t2 AS 
(
SELECT count(rental_id) AS cnt_rent, inventory_id
FROM rental 
GROUP BY inventory_id
),
t3 AS 
(
SELECT t1.rating, t1.inventory_id,
	CASE WHEN (t1.return_rate - t2.cnt_rent) >= 0 THEN 'niezwrocony' ELSE 'zwrocony' END AS status_zwrotu
FROM t2 t2
JOIN t1 t1
ON t1.inventory_id = t2.inventory_id 
),
t4 AS 
(
SELECT t3.rating, 
	count(r.rental_id) AS cnt,
	count (CASE WHEN t3.status_zwrotu = 'zwrocony' THEN t3.inventory_id end) AS good,
	count (CASE WHEN t3.status_zwrotu = 'niezwrocony' THEN t3.inventory_id end) AS bad
FROM rental r
JOIN t3 t3
	ON t3.inventory_id = r.inventory_id 
GROUP BY t3.rating
ORDER BY t3.rating
),
t5 AS 
(SELECT *, 
	good / sum(good) over()::NUMERIC good_distr,
	bad / sum(bad) over()::NUMERIC bad_distr
FROM t4
),

t6 AS
(SELECT *, 
	ln(good_distr/bad_distr) AS WOE,	
	(good_distr - bad_distr) AS "DG-DB",
	((good_distr - bad_distr)*(ln(good_distr/bad_distr))) AS "WOE*(DG-DB)"
FROM t5
),

t7 AS
(SELECT *,
	sum("WOE*(DG-DB)") over() AS IV
FROM t6
)

SELECT * FROM t7

-- ciekawostka: filmy, których zwrot nie był opóźniony, ale mają nadpłatę?

WITH t1 AS
(
SELECT f.rating, r.rental_id, f.film_id, i.inventory_id, f.rental_rate, p.amount,
	CASE WHEN p.amount - f.rental_rate > 0 THEN 'nadplata' 
		 WHEN p.amount - f.rental_rate = 0 THEN 'oplacony 'ELSE 'nieoplacony' END AS status_platnosci, 
	CASE WHEN f.rental_duration < date_part('day', return_date-rental_date) THEN 'opozniony' ELSE 'na_czas' end AS status_zwrotu
FROM film f
	JOIN inventory i 
	ON f.film_id = i.film_id 
	LEFT JOIN rental r
	ON i.inventory_id = r.inventory_id
	INNER JOIN payment p
	ON r.rental_id = p.rental_id 
ORDER BY f.film_id 
)
SELECT rating, sum(rental_rate) AS sum_rental_rate, sum(amount) AS sum_amount, (sum(amount) - sum(rental_rate)) AS amount_diff FROM t1
WHERE status_platnosci = 'nadplata'
AND status_zwrotu = 'na_czas'
GROUP BY rating 
ORDER BY rating


