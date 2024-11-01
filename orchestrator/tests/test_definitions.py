from dagster import Definitions
from orchestrator.definitions import defs  # Import your Definitions object


def test_dagster_definitions():
    # Test that the Definitions object is created correctly
    assert defs is not None
    assert isinstance(defs, Definitions)

    # Test that the assets are loaded correctly
    all_assets = defs.get_all_asset_specs()
    assert len(all_assets) > 0  # Ensure there are assets
