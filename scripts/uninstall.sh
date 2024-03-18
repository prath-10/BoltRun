#!/bin/bash

cat ../web/art/BoltRun.txt
echo "Uninstalling BoltRun"

if [ "$EUID" -ne 0 ]
  then
  echo "Error uninstalling BoltRun, Please run this script as root!"
  echo "Example: sudo ./uninstall.sh"
  exit
fi

echo "Stopping BoltRun"
docker stop boltrun_web_1 boltrun_db_1 boltrun_celery_1 boltrun_celery-beat_1 boltrun_redis_1 boltrun_tor_1 boltrun_proxy_1

if [[ $REPLY =~ ^[Yy]$ ]]
then
  echo "Stopping BoltRun"
  docker stop boltrun-web-1 boltrun-db-1 boltrun-celery-1 boltrun-celery-beat-1 boltrun-redis-1 boltrun-tor-1 boltrun-proxy-1
  echo "Stopped BoltRun"

  echo "Removing all containers related to BoltRun"
  docker rm boltrun-web-1 boltrun-db-1 boltrun-celery-1 boltrun-celery-beat-1 boltrun-redis-1 boltrun-tor-1 boltrun-proxy-1
  echo "Removed all containers related to BoltRun"

  echo "Removing all volumes related to BoltRun"
  docker volume rm boltrun_gf_patterns boltrun_github_repos boltrun_nuclei_templates boltrun_postgres_data boltrun_scan_results boltrun_tool_config boltrun_static_volume boltrun_wordlist
  echo "Removed all volumes related to BoltRun"

  echo "Removing all networks related to BoltRun"
  docker network rm boltrun_boltrun_network boltrun_default
  echo "Removed all networks related to BoltRun"
else
  exit 1
fi

echo "Finished Uninstalling."
