#!/bin/bash
# Install Postgresql
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list';
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -;
sudo apt-get update;
sudo apt-get install postgresql-13 --quiet --yes;
sudo apt -y install postgresql-common;
sudo sh /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh;
sudo sh -c "echo 'deb [signed-by=/usr/share/keyrings/timescale.keyring] https://packagecloud.io/timescale/timescaledb/ubuntu/ $(lsb_release -c -s) main' > /etc/apt/sources.list.d/timescaledb.list";
wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/timescale.keyring;
sudo apt-get update;

# Now install appropriate package for PG version
sudo apt -y install timescaledb-2-postgresql-13;
sudo timescaledb-tune --quiet --yes;
# Restart PostgreSQL instance
sudo service postgresql restart