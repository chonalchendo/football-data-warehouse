import json
import os
from pathlib import Path

import pandas as pd
from rich import print

# Dictionary mapping dataset filenames to their descriptions
DATASET_DESCRIPTIONS = {
    "player_defense.csv": "Player performance statistics from FBref including tackles, interceptions, and other metrics",
    "player_shooting.csv": "Player performance statistics from FBref including shots, goals, and other metrics",
    "player_passing.csv": "Player performance statistics from FBref including passes, key passes, and other metrics",
    "player_possession.csv": "Player performance statistics from FBref including dribbles, touches, and other metrics",
    "player_misc.csv": "Player performance statistics from FBref including fouls, cards, and other metrics",
    "player_gca.csv": "Player performance statistics from FBref including goal-creating actions",
    "player_keeper.csv": "Player performance statistics from FBref for goalkeepers",
    "player_keeper_adv.csv": "Advanced player performance statistics from FBref for goalkeepers",
    "player_passing_type.csv": "Player performance statistics from FBref including passes by type",
    "player_standard_stats.csv": "Player performance statistics from FBref including minutes played, goals, assists, and other metrics",
    "player_playing_time.csv": "Player performance statistics from FBref including minutes played, starts, and other metrics",
    "valuations.csv": "Historical market valuations from Transfermarkt and wage data from Fbref for football players",
    # Add descriptions for your other datasets here
}


def get_schema_fields(df: pd.DataFrame) -> list[dict]:
    """
    Generate schema fields for a dataframe.
    """
    fields = []
    for column in df.columns:
        dtype = str(df[column].dtype)
        # Convert numpy/pandas dtypes to Kaggle format
        if dtype.startswith("int") or dtype.startswith("float"):
            dtype = "number"
        elif dtype.startswith("datetime"):
            dtype = "datetime"
        else:
            dtype = "string"

        fields.append(
            {
                "name": column,
                "description": "",  # Can be filled in manually if needed
                "type": dtype,
            }
        )

    return fields


def generate_metadata(
    data_dir: str, output_file: str = "./data/public/dataset-metadata.json"
) -> None:
    """
    Generate metadata file in Kaggle's format.
    """
    metadata = {
        "title": "Football Data Warehouse",
        "subtitle": "Football statistics from Transfermarkt and FBref (top 5 leagues (2018-2024))",
        "description": "Parsed and cleaned football datasets from Transfermarkt and Fbref from the 2018/19 to 2024/25 season.\n ### Data Sources\n- [Transfermarkt](https://www.transfermarkt.com/)\n- [FBref](https://fbref.com/)\n\n",
        "id": "conalhenderson/football-data-warehouse",
        "licenses": [{"name": "CC0-1.0"}],
        "resources": [],
        "keywords": ["Football"],
    }

    # Process all CSV files
    data_path = Path(data_dir)
    print("Processing files:")

    for file_path in data_path.glob("**/*.csv"):
        relative_path = file_path.relative_to(data_path)
        print(f"- {relative_path}")

        resource = {
            "path": str(relative_path),
            "description": DATASET_DESCRIPTIONS.get(file_path.name, ""),
        }

        # Add schema for CSV files
        if file_path.suffix.lower() == ".csv":
            try:
                df = pd.read_csv(file_path)
                resource["schema"] = {"fields": get_schema_fields(df)}
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")

        metadata["resources"].append(resource)

    # Write metadata file
    with open(output_file, "w") as f:
        json.dump(metadata, f, indent=2)

    # Print summary
    print(f"\nGenerated metadata for {len(metadata['resources'])} files")

    # Print datasets missing descriptions
    missing_descriptions = [
        r["path"] for r in metadata["resources"] if not r["description"]
    ]
    if missing_descriptions:
        print("\nThe following files are missing descriptions:")
        for path in missing_descriptions:
            print(f'    "{os.path.basename(path)}": "",')


if __name__ == "__main__":
    # Update this path to match your data directory
    DATA_DIR = "./data/public"
    generate_metadata(DATA_DIR)
