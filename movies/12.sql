SELECT title
    FROM (
        SELECT title, movies.id as id1
        FROM movies
        JOIN stars ON movies.id = stars.movie_id
        JOIN people ON stars.person_id = people.id
        WHERE name = 'Helena Bonham Carter'
    )
    JOIN (
        SELECT movies.id as id2
        FROM movies
        JOIN stars ON movies.id = stars.movie_id
        JOIN people ON stars.person_id = people.id
        WHERE name = 'Johnny Depp'
    )
ON id1 = id2;

