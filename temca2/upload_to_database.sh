#!/bin/bash

# Get environment configuration or use defaults if unavailable.
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-catmaid}
DB_USER=${DB_USER:-catmaid_user}
DB_PASS=${DB_PASS:-catmaid_password}
CM_EXAMPLE_PROJECTS=${CM_EXAMPLE_PROJECTS:-true}

TIMEZONE=`readlink /etc/localtime | sed "s/.*\/\(.*\)$/\1/"`

# Check if the first argument begins with a dash. If so, prepend "platform" to
# the list of arguments.
if [ "${1:0:1}" = '-' ]; then
    set -- platform "$@"
fi

n_run=$(ls -l /.first_run_file | wc -l)
echo "Wait until database $DB_HOST:$DB_PORT is ready..."
until nc -z $DB_HOST $DB_PORT
do
    sleep 1
done

if [ $n_run -ne 2 ]; then
    echo "Need to recreate database."
    # Wait to avoid "panic: Failed to open sql connection pq: the database system is starting up"
    sleep 10
    PGPASSWORD=$DB_PASS psql -h $DB_HOST -U $DB_USER -d postgres -c "DROP DATABASE $DB_NAME;"
    sleep 1
    PGPASSWORD=$DB_PASS psql -h $DB_HOST -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME;"
    echo "Recreating database."
    PGPASSWORD=$DB_PASS psql -h $DB_HOST -U $DB_USER -d $DB_NAME < /v14.sql
    echo "Done."
    sleep 5
    echo "Initialised." > /.first_run_file/run
fi

bash /home/scripts/docker/catmaid-entry.sh -
