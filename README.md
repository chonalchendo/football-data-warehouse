# Data Football Warehouse

## Overview

This project is intended as a data warehouse for football data from various sources.

There are currently two sources of data:

- `Fbref`
- `Transfermarkt`

Essentially, public data is parsed from these two sources using the [football-data-extractor](https://github.com/chonalchendo/football-data-extractor) repository,
cleaned using `dbt` and `Duckdb`,and stored locally in `Duckdb` which acts as a local data warehouse. Both raw and processed
datasets are also stored in an Amazon S3 bucket.

The data pipeline is automated using `Dagster`.

## Setup

To setup the project in your local environment, follow the steps below:

1. Clone the repository

```bash
git clone https://github.com/chonalchendo/football-data-warehouse.git
```

2. Install uv for package management

```bash
pip install uv
```

3. Install the required packages using `uv install`

```bash
uv install
```
