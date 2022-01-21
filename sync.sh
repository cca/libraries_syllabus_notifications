#!/usr/bin/env bash
DEST="${HOME}/libraries_syllabus_notifications"
# pull from server
rsync -avz v1:"${DEST}/data" .
# push to server
rsync -avz --exclude '*.pyc' --exclude 'app/__pycache__' mail-log.sh app data v1:"${DEST}"
