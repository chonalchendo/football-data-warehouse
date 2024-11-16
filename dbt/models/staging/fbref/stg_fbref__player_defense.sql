with 
  raw_defense as (
    select * from {{ source("fbref", "player_defense") }}
  ),


-- create age range column
age_range as (
  select
    *,
    {{ age_range('age') }} as age_range
    from raw_defense
),

-- create general position column
general_position as (
  select
    *,
    {{ general_position('position') }} as general_position
    from age_range
),

-- add country and continent mapping
country_mapping as (
  select
    general_position.*,
    country_codes.country_name as country,
    country_codes.continent
  from general_position
  {{ add_country_mapping('general_position', 'nation') }}
)

select * from country_mapping


