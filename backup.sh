
# run this daily from cron
#
#  SHELL=/bin/sh
#  PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
#  17 21 * * *   root   /opt/netepi/backup.sh

BACKUP_DB_CMD=./netepi-db-backup.sh

BACKUP_DIR=./backup

cd /opt/netepi

[ ! -d "$BACKUP_DIR" ] && mkdir "$BACKUP_DIR"
"$BACKUP_DB_CMD" | (cd "$BACKUP_DIR"; gzip >"$(date '+db-%Y-%m-%d %H:%M:%S.sql.gz')")
