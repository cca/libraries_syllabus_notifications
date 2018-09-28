#!/usr/bin/env bash
# pull from server
rsync -avz dev:~/libraries_syllabus_notifications/data .
# push to server
rsync -avz data dev:~/libraries_syllabus_notifications
