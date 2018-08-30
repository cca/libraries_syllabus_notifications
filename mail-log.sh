#!/usr/bin/env bash
log stream --predicate  '(process == "smtpd") || (process == "smtp")' --info | ack 'to=<.*@cca\.edu>'
