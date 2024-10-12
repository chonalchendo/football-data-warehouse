import pandas as pd
from dagster import MetadataValue, asset, AssetExecutionContext, MaterializeResult

from src.extractors.transfermarkt import run_spider


season = "2025"

@asset(description='Club data crawled from Transfermarkt')
def clubs(context: AssetExecutionContext) -> None:
    context.log.info('Creating Clubs asset')
    
    run_spider('clubs', season)

    context.log.info(f'Clubs asset scraped for season {season}')


@asset(description='Squad data crawled from Transfermarkt') 
def squads(context: AssetExecutionContext) -> MaterializeResult:
    context.log.info('Creating Squads asset')

    run_spider('squads', season) 

    context.log.info(f'Squads asset scraped for season {season}')

    output_path = f'data/raw/transfermarkt/{season}/squads.json.gz'

    df = pd.read_json(output_path, lines=True)

    return MaterializeResult(
        metadata={
            'num_records': len(df),
            'preview': MetadataValue.md(df.head().to_markdown()),
            
        }
    )


    

