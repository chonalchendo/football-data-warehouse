{% macro create_general_position(pos) %}
    case
        when {{ pos }} is null then 'Unknown'
        when {{ pos }} = '' then 'Unknown'
        when left({{ pos }}, 1) = 'D' then 'Defender'
        when left({{ pos }}, 1) = 'M' then 'Midfielder'
        when left({{ pos }}, 1) = 'F' then 'Forward'
        when left({{ pos }}, 1) = 'G' then 'Goalkeeper'
        else 'Unknown'
    end
{% endmacro %}
{% macro create_age_range(age_column) %}
    case
        when cast({{ age_column }} as integer) < 20 then 'Under 20'
        when cast({{ age_column }} as integer) between 20 and 24 then '20-24'
        when cast({{ age_column }} as integer) between 25 and 29 then '25-29'
        when cast({{ age_column }} as integer) between 30 and 34 then '30-34'
        when cast({{ age_column }} as integer) between 35 and 39 then '35-39'
        when cast({{ age_column }} as integer) >= 40 then 'Over 40'
        else 'Unknown'
    end
{% endmacro %}

{% macro map_country_codes() %}  -- removed unused parameter
    select
        country_mapping.code,
        country_mapping.name as country_name,
        country_mapping.continent
    from {{ source('country_data', 'fifa_country_catalogue') }} as country_mapping
{% endmacro %}

{% macro add_country_mapping(table_alias, join_column) %}
    left join ({{ map_country_codes() }}) country_codes  -- now correct since parameter removed
        on {{ table_alias }}.{{ join_column }} = country_codes.code
{% endmacro %}

