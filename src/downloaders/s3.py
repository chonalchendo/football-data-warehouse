import argparse
import os

import polars as pl
import s3fs
from rich import print


def pull_data_from_s3(bucket_folder: str, output_folder: str) -> None:
    fs = s3fs.S3FileSystem(anon=False)
    bucket = f"s3://football-data-warehouse/{bucket_folder}"

    # output = f"{output_folder}"

    os.makedirs(output, exist_ok=True)

    files = fs.glob(bucket + "/**/*.parquet")

    files = [file for file in files if not any(x in file for x in ["wages", "squads"])]
    print(files)

    for file in files:
        print(f"Downloading file: {file}")
        # download each file to local data folder download each file to local data folder download each file to local data folder
        local_file_path = os.path.join(
            output_folder, os.path.basename(file).replace(".parquet", ".csv")
        )
        print(local_file_path)
        df = pl.read_parquet(f"s3://{file}")
        df.write_csv(local_file_path)

    print("All files downloaded to local folder.")


if __name__ == "__main__":
    parse = argparse.ArgumentParser()

    parse.add_argument("--folder", type=str, help="Folder to pull from s3")
    parse.add_argument("--output", type=str, help="Output folder")

    args = parse.parse_args()
    folder = args.folder
    output = args.output

    print(f"Pulling data from s3 folder: {folder}")
    pull_data_from_s3(bucket_folder=folder, output_folder=output)
    print("Data pulled from s3 successfully")
