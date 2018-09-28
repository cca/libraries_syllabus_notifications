#!/usr/bin/env bash
sudo tail -f /var/log/exim4/mainlog | ack '=> .*@cca\.edu'
