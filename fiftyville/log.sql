-- Keep a log of any SQL queries you execute as you solve the mystery.

-- See structure of database
.schema;

-- See crime reports from
SELECT description
FROM crime_scene_reports
WHERE day = 28
AND month = 7
AND year = 2021
AND street = 'Humphrey Street';

-- See interview statements that mention the bakery
SELECT transcript, id
FROM interviews
WHERE transcript
LIKE '%bakery%';

-- See security log arrounf 10 minutes after theft
SELECT activity, license_plate
FROM bakery_security_logs
WHERE day = 28
AND month = 7
AND year = 2021
AND hour = 10
AND minute BETWEEN 15 and 30;

-- See atm record
SELECT account_number
FROM atm_transactions
WHERE day = 28
AND month = 7
AND year = 2021
AND transaction_type = 'withdraw'
AND atm_location = 'Leggett Street';

-- See phone calls
SELECT caller, receiver, duration
FROM phone_calls
WHERE day = 28
AND month = 7
AND year = 2021
AND duration < 60;

-- First flight leaving fiftyville in the morning
SELECT id, hour, minute
FROM flights
WHERE origin_airport_id IN
    (
        SELECT id
        FROM airports
        WHERE city = 'Fiftyville'
    )
AND day = 29
AND month = 7
AND year = 2021
ORDER BY hour, minute
LIMIT 1;

-- Find people whose license plate, passport number, personID and phone number match suspects
SELECT *
FROM people
WHERE license_plate IN
    (
        SELECT license_plate
        FROM bakery_security_logs
        WHERE day = 28
        AND month = 7
        AND year = 2021
        AND hour = 10
        AND minute BETWEEN 15 and 30
    )
AND phone_number IN
    (
        SELECT caller
        FROM phone_calls
        WHERE day = 28
        AND month = 7
        AND year = 2021
        AND duration < 60
    )
AND passport_number in
    (
        SELECT passport_number
        FROM passengers
        WHERE flight_id in
            (
                SELECT id
                FROM flights
                WHERE origin_airport_id IN
                    (
                        SELECT id
                        FROM airports
                        WHERE city = 'Fiftyville'
                    )
                AND day = 29
                AND month = 7
                AND year = 2021
                ORDER BY hour, minute
                LIMIT 1
            )
    )
AND id IN
    (
        SELECT person_id
        FROM bank_accounts
        WHERE account_number IN
        (
            SELECT account_number
            FROM atm_transactions
            WHERE day = 28
            AND month = 7
            AND year = 2021
            AND transaction_type = 'withdraw'
            AND atm_location = 'Leggett Street'
        )
    )
;

-- Find city to where Bruce traveled to
SELECT city
FROM airports
WHERE id IN
(
    SELECT destination_airport_id
    FROM flights
    WHERE origin_airport_id IN
        (
            SELECT id
            FROM airports
            WHERE city = 'Fiftyville'
        )
    AND day = 29
    AND month = 7
    AND year = 2021
    ORDER BY hour, minute
    LIMIT 1
);

-- Find to whom bruce called in the morning of the theft
SELECT name
FROM people
WHERE phone_number IN
(
    SELECT receiver
    FROM phone_calls
    WHERE day = 28
    AND month = 7
    AND year = 2021
    AND duration < 60
    AND caller IN
        (
            SELECT phone_number
            FROM people
            WHERE name = 'Bruce'
        )
);





