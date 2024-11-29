{% macro parse_currency_amounts(column_name) %}
        CAST(REPLACE(REPLACE(REGEXP_EXTRACT({{ column_name }}, '€ ([0-9,]+)'), ',', ''), '€ ', '') AS INTEGER) AS {{ column_name }}_eur,
        CAST(REPLACE(REPLACE(REGEXP_EXTRACT({{ column_name }}, '£ ([0-9,]+)'), ',', ''), '£ ', '') AS INTEGER) AS {{ column_name }}_gbp,
        CAST(REPLACE(REPLACE(REGEXP_EXTRACT({{ column_name }}, '\$([0-9,]+)'), ',', ''), '$', '') AS INTEGER) AS {{ column_name }}_usd
{% endmacro %}

