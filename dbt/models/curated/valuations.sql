with
squads as (
    select * from {{ ref('stg_transfermarkt__squads') }}
),

player_wages as (
    select * from {{ ref('stg_fbref__player_wages') }}
),

-- join data on name, season, and squad
valuations_data as (
    select 
        squads.*,
        player_wages.*
    from squads
    inner join player_wages on
    squads.player = player_wages.player and
    squads.season = player_wages.season and
    squads.squad = player_wages.squad
)

select  
    player,
    age,
    dob,
    height,
    country,
    squad,
    current_club,
    signed_from,
    position,
    squad_number,
    market_value_eur_mill,
    signing_fee_eur_mill,
    weekly_wages_gbp,
    weekly_wages_usd,
    weekly_wages_eur,
    annual_wages_gbp,
    annual_wages_usd,
    annual_wages_eur,
    season
from valuations_data



