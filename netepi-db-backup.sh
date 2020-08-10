#
# backup the entire docker db as a stream of sql to stdout
#
# Example:
#   ./netepi-db-backup.sh | gzip >"$(date '+db-%Y-%m-%d %H:%M:%S.sql.gz')"
#
# To restore:
#   gunzip <"db-2020-08-10 14:36:02.sql.gz" | docker-compose exec db psql -U postgres
#
# (from https://stackoverflow.com/questions/24718706/backup-restore-a-dockerized-postgresql-database)

docker-compose exec db pg_dumpall -c -U postgres