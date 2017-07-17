### Instructions for initializing Postgres container

FROM postgres

# Add SQL file to 'docker-entrypoint-initdb.d' directory so
#       it will execute on init
ADD create.sql /docker-entrypoint-initdb.d
