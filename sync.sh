#!/usr/bin/env bash
DEST="${HOME}/libraries_syllabus_notifications"
# pull from server
rsync -avz dev:"${DEST}/data" .
# push to server
rsync -avz --exclude '*.pyc' --exclude 'app/__pycache__' app data dev:"${DEST}"
