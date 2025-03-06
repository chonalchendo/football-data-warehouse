{{ process_player_stats('player_wages') }},

-- load in transfermarkt squad names
tmarket_squad_names as (
    select * from {{ source('seeds', 'tmarket_squad_names') }}
),


-- add transfermarkt squad names
mapped_squad_names as (
    select
        pd.*,
        tmarket.tmarket_names as tmarket_squad
    from country_mapping pd
    inner join tmarket_squad_names tmarket
    on pd.squad = tmarket.fbref_teams
),


-- extract wage values
wage_values as (
    select
        mapped_squad_names.*,
        {{ parse_currency_amounts('weekly_wages') }}
    from mapped_squad_names
),

-- extract annual wage values
annual_wage_values as (
    select
        wage_values.*,
        {{ parse_currency_amounts('annual_wages') }}
    from wage_values
)


select 
    rk :: integer as fbref_id,
    player,
    squad,
    tmarket_squad,
    weekly_wages_gbp :: integer as weekly_wages_gbp,
    weekly_wages_usd :: integer as weekly_wages_usd,
    weekly_wages_eur :: integer as weekly_wages_eur,
    annual_wages_gbp :: integer as annual_wages_gbp,
    annual_wages_eur :: integer as annual_wages_eur,
    annual_wages_usd :: integer as annual_wages_usd,
    season :: integer as season
from annual_wage_values;
