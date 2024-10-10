from dagster import asset, AssetExecutionContext 

from src.extractors.transfermarkt import run_spider


season = "2023"

@asset(description='Club data crawled from Transfermarkt')
def clubs(context: AssetExecutionContext) -> None:
    context.log.info('Creating Clubs asset')
    
    run_spider('clubs', season)

    context.log.info(f'Clubs asset scraped for season {season}')


@asset(deps=[clubs], description='Squad data crawled from Transfermarkt') 
def squads(context: AssetExecutionContext) -> None:
    context.log.info('Creating Squads asset')

    run_spider('squads', season) 

    context.log.info(f'Squads asset scraped for season {season}')

    

