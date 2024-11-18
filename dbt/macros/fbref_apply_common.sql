{% macro process_player_stats(table_name) %}

with age_range_data as (
    select
        *,
        {{ create_age_range('age') }} as age_range
    from {{ table_name }}  -- Need double curly braces for table_name parameter
),

general_position_data as (
    select
        *,
        {{ create_general_position('position') }} as general_position
    from age_range_data
),

country_mapping as (
    select
        general_position_data.*,  -- Need to use the correct CTE name
        country_codes.country_name as country,
        country_codes.continent
    from general_position_data
    {{ add_country_mapping('general_position_data', 'nation') }}  -- Need to use correct CTE name
)

select * from country_mapping

{% endmacro %}

