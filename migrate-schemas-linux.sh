#!/usr/bin/env bash

# === Config ===

PYTHON="python3"

# === Code ===

source .env

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR"

source env/bin/activate

PYTHON="python3"

function list_schemas() {
	PGPASSWORD="$DB_PASS" psql \
		--host="$DB_HOST" \
		--port="$DB_PORT" \
		--user="$DB_USERNAME" \
		--no-password "$DB_NAME" \
		-c "copy (select distinct schema_name from public.home_client where schema_name is not null) to stdout with null as ''"
}

for schema in $( list_schemas ); do
	echo "Migrating schema '$schema'..."
	$PYTHON manage.py migrate_schemas --schema="$schema"
done

echo "Migrated all schemas"
