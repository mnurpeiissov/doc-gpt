#! /usr/bin/env bash

set -e
set -x

python /app/scripts/create_vector_tables.py

echo ALL GOOD!