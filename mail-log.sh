#!/usr/bin/env bash
if [ $(command -v grc) ]; then
    grc tail -f /var/log/mail.log -n200
else
    tail -f /var/log/mail.log -n200
fi
