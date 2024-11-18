{% macro parse_currency_amounts(column_name) %}
    REGEXP_REPLACE(REGEXP_EXTRACT({{ column_name }}, '£\s*([\d,]+)'), '[,]', '')::INTEGER as {{ column_name }}_gbp,
    REGEXP_REPLACE(REGEXP_EXTRACT({{ column_name }}, '€\s*([\d,]+)'), '[,]', '')::INTEGER as {{ column_name }}_eur,
    REGEXP_REPLACE(REGEXP_EXTRACT({{ column_name }}, '\$\s*([\d,]+)'), '[,]', '')::INTEGER as {{ column_name }}_usd,
{% endmacro %}