WITH squads_data AS (
    SELECT * FROM {{ source('transfermarkt', 'squads') }}
),

-- Clean squad numbers
clean_squad_numbers AS (
    SELECT
        *,
        CASE WHEN number = '-' THEN '0' ELSE number END AS clean_squad_num 
    FROM squads_data 
),

-- Clean signed from
clean_signed_from AS (
    SELECT
        *,
        CASE WHEN signed_from IS NULL then 'Unknown' ELSE signed_from END AS clean_signed_from
    FROM clean_squad_numbers
),

-- Clean market values
clean_market_values AS (
    SELECT
        *,
        CASE 
            WHEN value LIKE '%k' THEN REPLACE(REPLACE(value, '€', ''), 'k', '') :: FLOAT / 1000
            WHEN value LIKE '%m' THEN REPLACE(REPLACE(value, '€', ''), 'm', '') :: FLOAT
            WHEN value LIKE '%bn' THEN REPLACE(REPLACE(value, '€', ''), 'bn', '') :: FLOAT * 1000
            WHEN value = '-' THEN NULL
            ELSE REPLACE(value, '€', '') :: FLOAT / 1000000
        END AS market_value_eur_mill
    FROM clean_squad_numbers 
),


-- Clean signing fee
clean_signing_fee AS (
    SELECT
        *,
        CASE 
            WHEN signing_fee LIKE '%k' THEN REPLACE(REPLACE(REPLACE(signing_fee, '€', ''), 'Ablöse ', ''), 'k', '') :: FLOAT / 1000
            WHEN signing_fee LIKE '%m' THEN REPLACE(REPLACE(REPLACE(signing_fee, '€', ''), 'Ablöse ', ''), 'm', '') :: FLOAT
            WHEN signing_fee LIKE '%bn' THEN REPLACE(REPLACE(REPLACE(signing_fee, '€', ''), 'Ablöse ', ''), 'bn', '') :: FLOAT * 1000
            WHEN signing_fee IN ('-', '?', 'free transfer', 'draft') THEN 0
            WHEN signing_fee = '' THEN NULL
            ELSE REPLACE(REPLACE(signing_fee, '€', ''), 'Ablöse ', '') :: FLOAT / 1000000
        END AS signing_fee_eur_mill
    FROM clean_market_values
),

-- Clean height
clean_height AS (
    SELECT
        *,
        CASE 
            WHEN height = '-' THEN NULL
            WHEN height LIKE '%N/A%' THEN NULL
            ELSE REPLACE(REPLACE(height, 'm', ''), ',', '.') :: FLOAT
        END AS clean_height
    FROM clean_signing_fee 
),

-- Clean position
clean_position AS (
    SELECT
        *,
        CASE
            WHEN position = 'Mittelfeld' THEN 'Central-Midfield'
            ELSE REGEXP_REPLACE(position, '([a-z])([A-Z])', '\1-\2')
        END AS clean_position
    FROM clean_height
)

-- Final select
SELECT
    tm_id :: INTEGER as tm_id,
    tm_name,
    name as player,
    season :: INTEGER as season,
    country,
    foot,
    age :: INTEGER as age,
    squad,
    dob,
    current_club,
    signed_from,
    clean_position AS position,
    clean_squad_num :: INTEGER AS squad_number,
    market_value_eur_mill,
    signing_fee_eur_mill,
    clean_height AS height
FROM clean_position
