#!/bin/bash

set -ex

PROJECT_HOME=/app
DAGSTER_HOME=/dagster_home
BRANCH=$1
COMMAND=$2

shift 2

# Export Dagster home environment variable
# export DAGSTER_HOME=$DAGSTER_HOME

if ! [ -d $PROJECT_HOME ]; then
    echo "Setting up project dir"
    if ! [ -z ${BRANCH+x} ]; then
        git clone --branch $BRANCH https://github.com/chonalchendo/football-data-warehouse.git
        cd $PROJECT_HOME
        if ! [ -z ${DAGSTER_HOME+x} ]; then
            echo "Setting up Dagster home"
            cp $PROJECT_HOME/orchestrator/dagster.yaml $DAGSTER_HOME # Copy the dagster.yaml file to the Dagster home
            rm -rf $PROJECT_HOME/orchestrator/dagster.yaml # Remove the dagster.yaml from the project home
            echo "Dagster home setup complete"
        else
            echo "DAGSTER_HOME is required to bootstrap the environment"
            exit 1
        fi
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