SELECT title,rating
FROM ratings
JOIN movies
ON movies.id = ratings.movie_id
WHERE movies.year = 2010 AND rating NOT NULL
ORDER BY rating DESC, title;