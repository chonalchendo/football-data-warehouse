{#
    Export a model to the prep folder in a Parquet format.

    Arguments:
      - relation: the model to be exported
#}
{% macro export_to_parquet(relation) %}
    {% call statement(name, fetch_result=True) %}
        COPY (SELECT * FROM {{ relation }}) 
        TO '../data/prep/{{ relation.name }}.parquet' 
        (FORMAT 'parquet')
    {% endcall %}
{% endmacro %}