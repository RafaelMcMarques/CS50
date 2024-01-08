SELECT name
FROM people
WHERE id IN
(
    SELECT DISTINCT(personID)
    FROM
    (
        SELECT movie_id as kevinMovieID
        FROM stars
        JOIN people ON people.id = stars.person_id
        WHERE name = 'Kevin Bacon' AND birth = '1958'
    )
    JOIN
    (
        SELECT name, movie_id as personMovieID, people.id as personID
        FROM stars
        JOIN people ON people.id = stars.person_id
    )
    ON personMovieID = kevinMovieID
    WHERE name != 'Kevin Bacon'
)
ORDER BY name;
