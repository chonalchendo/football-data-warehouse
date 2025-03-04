import os

import polars as pl
import s3fs
from dagster import ConfigurableIOManager, InputContext, OutputContext


class PartitionedParquetIOManager(ConfigurableIOManager):
    storage_options: dict | None = None

    @property
    def _base_path(self):
        return NotImplementedError()

    def _file_system(self):
        if "s3://" in self._base_path:
            return NotImplementedError()
        return s3fs.S3FileSystem()

    def handle_output(self, context: OutputContext, obj: pl.DataFrame) -> None:
        filepath = self._get_path(context=context)

        if "s3://" in filepath:
            fs = self._file_system()
            with fs.open(filepath, "wb") as f:
                obj.write_parquet(f)
        else:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            obj.write_parquet(filepath)

    def load_input(self, context: InputContext) -> pl.DataFrame:
        # filepath = self._base_path + context.season + context.name
        filepath = self._get_path(context=context)

        if "s3://" in filepath and self.storage_options:
            return pl.scan_parquet(
                filepath, storage_options=self.storage_options
            ).collect()
        return pl.read_parquet(filepath)

    def _get_path(self, context: OutputContext) -> str:
        asset = context.asset_key.path[-1]
        group = context.asset_key.path[-2]
        folder = context.asset_key.path[-3]
        # folder = context.definition_metadata.get("folder")
        # group = context.definition_metadata.get("group")

        output_path = os.path.join(self._base_path, folder, group, f"{asset}.parquet")

        if context.has_asset_partitions:
            season = context.partition_key
            output_path = os.path.join(
                self._base_path, folder, group, season, f"{asset}.parquet"
            )

        return output_path


class S3PartitionedParquetIOManager(PartitionedParquetIOManager):
    s3_bucket: str

    @property
    def _base_path(self) -> str:
        return f"s3://{self.s3_bucket}/"

    def _file_system(self):
        return s3fs.S3FileSystem(
            key=self.storage_options["aws_secret_key_id"],
            secret=self.storage_options["aws_secret_access_key"],
        )
