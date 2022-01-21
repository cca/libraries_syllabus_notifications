#!/usr/bin/env bash
sudo tail -f -n 100 /var/log/mail.log | ack ' .*@cca\.edu'
