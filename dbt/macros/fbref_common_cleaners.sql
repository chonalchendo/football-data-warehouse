{% macro process_player_stats(table_name) %}
with raw_stats as (
    select 
        * exclude (pos),
        pos as position
    from {{ source('fbref', table_name) }}
),

country_codes as (
    select
        code,
        name as country,
        continent
    from {{ source('seeds', 'fifa_country_catalogue') }}
),

age_range_data as (
    select
        *,
        case
            when cast(age as integer) < 20 then 'Under 20'
            when cast(age as integer) between 20 and 24 then '20-24'
            when cast(age as integer) between 25 and 29 then '25-29'
            when cast(age as integer) between 30 and 34 then '30-34'
            when cast(age as integer) between 35 and 39 then '35-39'
            when cast(age as integer) >= 40 then 'Over 40'
            else 'Unknown'
        end as age_range
    from raw_stats
),

general_position_data as (
    select
        *,
        case
            when position is null then 'Unknown'
            when position = '' then 'Unknown'
            when left(position, 1) = 'D' then 'Defender'
            when left(position, 1) = 'M' then 'Midfielder'
            when left(position, 1) = 'F' then 'Forward'
            when left(position, 1) = 'G' then 'Goalkeeper'
            else 'Unknown'
        end as general_position
    from age_range_data
),

country_mapping as (
    select
        general_position_data.*,
        country_codes.country,
        country_codes.continent
    from general_position_data
    left join country_codes
    on general_position_data.nation = country_codes.code
)
{% endmacro %}