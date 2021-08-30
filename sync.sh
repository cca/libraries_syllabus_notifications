#!/usr/bin/env bash
DEST="${HOME}/libraries_syllabus_notifications"
# @TODO can we combine these 3 rsyncs so I do the SSH 2FA fewer times?
# pull from server
rsync -avz dev:"${DEST}/data" .
# push to server
rsync -avz data dev:"${DEST}"
rsync -avz --exclude '*.pyc' --exclude 'app/__pycache__' app dev:"${DEST}"
