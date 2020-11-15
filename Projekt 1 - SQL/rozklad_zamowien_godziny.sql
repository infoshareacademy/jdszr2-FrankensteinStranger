with rentals_by_hour as (
select 
	date_part('hour', rental_date) as hours,
	inventory_id,
	c.name as category
from rental
	left join inventory i2 using(inventory_id)
	left join film f2 using(film_id)
	left join film_category fc using(film_id)
	left join category c using(category_id))

select 
	category,
	hours,
	count(inventory_id) as rentals
from rentals_by_hour
group by 1,2
order by 1,2


----
