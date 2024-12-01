#!/bin/bash

set -ex

PROJECT_HOME=/app/football-data-warehouse
DAGSTER_HOME=$PROJECT_HOME/orchestrator
BRANCH=$1
COMMAND=$2

shift 2

# Export Dagster home environment variable
export DAGSTER_HOME=$DAGSTER_HOME

if ! [ -d $PROJECT_HOME ]; then
    echo "Setting up project dir"
    if ! [ -z ${BRANCH+x} ]; then
        git clone --branch $BRANCH https://github.com/chonalchendo/football-data-warehouse.git
        cd $PROJECT_HOME
    else
        echo "BRANCH is required to bootstrap the environment"
        exit 1
    fi
fi

cd $PROJECT_HOME
if $COMMAND "$@" ; then
    echo "Job succeeded"
    exit 0
else
    echo "Job failed"
    exit 1
fi